import re
from functools import lru_cache

import ftfy

from ekphrasis.classes.exmanager import ExManager
from ekphrasis.classes.segmenter import Segmenter
from ekphrasis.classes.spellcorrect import SpellCorrector
from ekphrasis.utils.nlp import unpack_contractions


# noinspection PyPackageRequirements
class TextPreProcessor:
    def __init__(self, **kwargs):
        """
        Kwargs:
            omit (list): choose what tokens that you want to omit from the text.
                possible values: ['email', 'percent', 'money', 'phone', 'user',
                    'time', 'url', 'date', 'hashtag']
                Important Notes:
                            1 - put url at front, if you plan to use it.
                                Messes with the regexes!
                            2 - if you use hashtag then unpack_hashtags will
                                automatically be set to False

            normalize (list): choose what tokens that you want to normalize
                from the text.
                possible values: ['email', 'percent', 'money', 'phone', 'user',
                    'time', 'url', 'date', 'hashtag']
                for example: myaddress@mysite.com will be transformed to <email>
                Important Notes:
                            1 - put url at front, if you plan to use it.
                                Messes with the regexes!
                            2 - if you use hashtag then unpack_hashtags will
                                automatically be set to False

            unpack_contractions (bool): Replace *English* contractions in
                ``text`` str with their unshortened forms
                for example: can't -> can not, wouldn't -> would not, and so on...

            unpack_hashtags (bool): split a hashtag to it's constituent words.
                for example: #ilikedogs -> i like dogs

            annotate (list): add special tags to special tokens.
                possible values: ['hashtag', 'allcaps', 'elongated', 'repeated']
                for example: myaddress@mysite.com -> myaddress@mysite.com <email>

            tokenizer (callable): callable function that accepts a string and
                returns a list of strings if no tokenizer is provided then
                the text will be tokenized on whitespace

            segmenter (str): define the statistics of what corpus you would
                like to use [english, twitter]

            corrector (str): define the statistics of what corpus you would
                like to use [english, twitter]

            all_caps_tag (str): how to wrap the capitalized words
                values [single, wrap, every]
                Note: applicable only when `allcaps` is included in annotate[]
                    - single: add a tag after the last capitalized word
                    - wrap: wrap all words with opening and closing tags
                    - every: add a tag after each word

            spell_correct_elong (bool): choose if you want to perform
                spell correction after the normalization of elongated words.
                * significantly affects performance (speed)

            spell_correction (bool): choose if you want to perform
                spell correction to the text
                * significantly affects performance (speed)

            fix_text (bool): choose if you want to fix bad unicode terms and
                html entities.
        """
        self.omit = kwargs.get("omit", {})
        self.backoff = kwargs.get("normalize", {})
        self.include_tags = kwargs.get("annotate", {})
        self.unpack_contractions = kwargs.get("unpack_contractions", False)
        self.tokenizer = kwargs.get("tokenizer", None)
        self.dicts = kwargs.get("dicts", None)
        self.spell_correction = kwargs.get("spell_correction", False)
        self.spell_correct_elong = kwargs.get("spell_correct_elong", False)
        self.fix_text = kwargs.get("fix_bad_unicode", False)
        self.unpack_hashtags = kwargs.get("unpack_hashtags", False)
        self.segmenter_corpus = kwargs.get("segmenter", "english")
        self.corrector_corpus = kwargs.get("corrector", "english")
        self.all_caps_tag = kwargs.get("all_caps_tag", "wrap")
        self.mode = kwargs.get("mode", "normal")

        if self.unpack_hashtags:
            self.segmenter = Segmenter(corpus=self.segmenter_corpus)
        if self.mode != "fast":
            self.spell_corrector = SpellCorrector(corpus=self.corrector_corpus)

        self.regexes = ExManager().get_compiled()
        if 'hashtag' in self.omit or 'hashtag' in self.backoff:
            print("You can't omit/backoff and unpack hashtags!\n "
                  "unpack_hashtags will be set to False")
            self.unpack_hashtags = False

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    @staticmethod
    def add_special_tag(m, tag, mode="single"):

        if isinstance(m, str):
            text = m
        else:
            text = m.group()

        if mode == "single":
            return " {} <{}> ".format(text, tag)
        elif mode == "wrap":
            return " ".join([" <{}> {} </{}> ".format(tag, text, tag)]) + " "
        elif mode == "every":
            tokens = text.split()
            processed = " ".join([" {} <{}> ".format(t, tag)
                                  for t in tokens])
            return " " + processed + " "

    @lru_cache(maxsize=65536)
    def handle_hashtag_match(self, m):
        """
        Break a string to its constituent words (using Viterbi algorithm)
        """
        text = m.group()[1:]

        # todo:simplify routine
        if text.islower():
            expanded = self.segmenter.segment(text)
            expanded = " ".join(expanded.split("-"))
            expanded = " ".join(expanded.split("_"))
            # print(m.group(), " - ", expanded)
            # with open("analysis/segmenter_" +
            # self.segmenter_corpus + ".txt", "a") as f:
            #     f.write(m.group() + "\t" + expanded + "\n")

        else:
            # split words following CamelCase convention
            expanded = self.regexes["camel_split"].sub(r' \1', text)
            expanded = expanded.replace("-", "")
            expanded = expanded.replace("_", "")
            # print(m.group(), " - ", expanded)

        if "hashtag" in self.include_tags:
            expanded = self.add_special_tag(expanded, "hashtag", mode="wrap")

        return expanded

    def handle_elongated_match(self, m):
        text = m.group()

        # normalize to at most 2 repeating chars
        text = self.regexes["normalize_elong"].sub(r'\1\1', text)

        normalized = self.spell_corrector.normalize_elongated(text)
        if normalized:
            text = normalized

        # try to spell correct the word
        if self.spell_correct_elong:
            text = self.spell_corrector.correct_word(text, assume_wrong=True,
                                                     fast=True)
            # with open("analysis/spell_corrector_" +
            # self.corrector_corpus + ".txt", "a") as f:
            #     f.write(m.group() + " - " + text + "\n")

            # print(m.group(), "-", text)
        if "elongated" in self.include_tags:
            text = self.add_special_tag(text, "elongated")

        return text

    @lru_cache(maxsize=65536)
    def handle_repeated_puncts(self, m):
        """
        return the sorted set so mathes random combinations of puncts
        will be mapped to the same token
        "!??!?!!", "?!!!!?!", "!!?", "!?!?" --> "?!"
        "!...", "...?!" --> ".!"
        :param m:
        :return:
        """
        text = m.group()
        text = "".join(sorted(set(text), reverse=True))

        if "repeated" in self.include_tags:
            text = self.add_special_tag(text, "repeated")

        return text

    @lru_cache(maxsize=65536)
    def handle_generic_match(self, m, tag, mode="every"):
        """

        Args:
            m ():
            tag ():
            mode ():

        Returns:

        """
        text = m.group()
        text = self.add_special_tag(text, tag, mode=mode)

        return text

    @lru_cache(maxsize=65536)
    def handle_emphasis_match(self, m):
        """
        :param m:
        :return:
        """
        text = m.group().replace("*", "")
        if "emphasis" in self.include_tags:
            text = self.add_special_tag(text, "emphasis")

        return text

    @staticmethod
    def dict_replace(wordlist, _dict):
        return [_dict[w] if w in _dict else w for w in wordlist]

    @staticmethod
    def remove_hashtag_allcaps(wordlist):
        in_hashtag = False
        _words = []
        for word in wordlist:

            if word == "<hashtag>":
                in_hashtag = True
            elif word == "</hashtag>":
                in_hashtag = False
            elif word in {"<allcaps>", "</allcaps>"} and in_hashtag:
                continue

            _words.append(word)

        return _words

    def pre_process_doc(self, doc):

        doc = re.sub(r' +', ' ', doc)  # remove repeating spaces

        # ###########################
        # # fix bad unicode
        # ###########################
        # if self.fix_bad_unicode:
        #     doc = textacy.preprocess.fix_bad_unicode(doc)
        #
        # ###########################
        # # fix html leftovers
        # ###########################
        # doc = html.unescape(doc)

        ###########################
        # fix text
        ###########################
        if self.fix_text:
            doc = ftfy.fix_text(doc)

        ###########################
        # BACKOFF & OMIT
        ###########################
        for item in self.backoff:
            # better add an extra space after the match.
            # Just to be safe. extra spaces will be normalized later anyway
            doc = self.regexes[item].sub(lambda m: " " + "<" + item + ">" + " ",
                                         doc)
        for item in self.omit:
            doc = doc.replace("<" + item + ">", '')

        ###########################
        # unpack hashtags
        ###########################
        if self.unpack_hashtags:
            doc = self.regexes["hashtag"].sub(
                lambda w: self.handle_hashtag_match(w), doc)

        ###########################
        # handle special cases
        ###########################
        if self.mode != "fast":
            if "allcaps" in self.include_tags:
                doc = self.regexes["allcaps"].sub(
                    lambda w: self.handle_generic_match(w, "allcaps",
                                                        mode=self.all_caps_tag),
                    doc)

            if "elongated" in self.include_tags:
                doc = self.regexes["elongated"].sub(
                    lambda w: self.handle_elongated_match(w), doc)

            if "repeated" in self.include_tags:
                doc = self.regexes["repeat_puncts"].sub(
                    lambda w: self.handle_repeated_puncts(w), doc)

            if "emphasis" in self.include_tags:
                doc = self.regexes["emphasis"].sub(
                    lambda w: self.handle_emphasis_match(w), doc)

            if "censored" in self.include_tags:
                doc = self.regexes["censored"].sub(
                    lambda w: self.handle_generic_match(w, "censored"), doc)

        ###########################
        # unpack contractions: i'm -> i am, can't -> can not...
        ###########################

        # remove textacy dependency
        if self.unpack_contractions:
            doc = unpack_contractions(doc)

        # omit allcaps if inside hashtags
        doc = re.sub(r' +', ' ', doc)  # remove repeating spaces
        # doc = re.sub(r'<hashtag><allcaps>', '<hashtag>', doc)  # remove repeating spaces
        # doc = doc.replace('<hashtag> <allcaps>', '<hashtag>')
        # doc = doc.replace('</allcaps> </hashtag>', '</hashtag>')

        ###########################
        # Tokenize
        ###########################
        doc = self.remove_hashtag_allcaps(doc.split())
        doc = " ".join(doc)  # normalize whitespace
        if self.tokenizer:
            doc = self.tokenizer(doc)

            # Replace tokens with special dictionaries (slang,emoticons ...)
            # todo: add spell check before!
            if self.dicts:
                for d in self.dicts:
                    doc = self.dict_replace(doc, d)

        return doc

    def pre_process_docs(self, docs, lazy=True):
        from tqdm import tqdm
        for d in tqdm(docs, desc="PreProcessing..."):
            yield self.pre_process_doc(d)
