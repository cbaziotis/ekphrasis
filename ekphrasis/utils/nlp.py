import itertools
import re

import nltk
import numpy
from nltk.corpus import sentiwordnet as swn
from termcolor import cprint

wordnet_lemmatizer = nltk.WordNetLemmatizer()
# additional negations: nowhere

negation_words = {"'t", "ain't", 'aint', "aren't", 'arent', 'cant',
                  "didn't", 'didnt', "doesn't", 'doesnt', "don't", 'dont',
                  "hadn't", 'hadnt', "hasn't", 'hasnt', "haven't", 'havent',
                  "isn't", 'isnt',
                  'never', 'no', 'none', 'noone', 'not', 'nothing', 'wont', }
negation_modals = {"couldn't", 'couldnt', "shouldn't", 'shouldnt', "wouldn't",
                   'wouldnt'}
contrast_words = {"but", "although", "though", "however", "despite", "whereas",
                  "while", "unlike", "still"}
neg_puncts = {"\n", ".", "?", ":", "..."}


def unpack_contractions(text):
    """
    Replace *English* contractions in ``text`` str with their unshortened forms.
    N.B. The "'d" and "'s" forms are ambiguous (had/would, is/has/possessive),
    so are left as-is.

    ---------
    ---------

    Important Note: The function is taken from textacy (https://github.com/chartbeat-labs/textacy).

    See textacy.preprocess.unpack_contractions(text)
    -> http://textacy.readthedocs.io/en/latest/api_reference.html#textacy.preprocess.unpack_contractions


    The reason that textacy is not added as a dependency is to avoid having the user to install it's dependencies (such as SpaCy),
    in order to just use this function.

    """
    # standard
    text = re.sub(
        r"(\b)([Aa]re|[Cc]ould|[Dd]id|[Dd]oes|[Dd]o|[Hh]ad|[Hh]as|[Hh]ave|[Ii]s|[Mm]ight|[Mm]ust|[Ss]hould|[Ww]ere|[Ww]ould)n't",
        r"\1\2 not", text)
    text = re.sub(
        r"(\b)([Hh]e|[Ii]|[Ss]he|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou)'ll",
        r"\1\2 will", text)
    text = re.sub(r"(\b)([Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou)'re", r"\1\2 are",
                  text)
    text = re.sub(
        r"(\b)([Ii]|[Ss]hould|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Ww]ould|[Yy]ou)'ve",
        r"\1\2 have", text)
    # non-standard
    text = re.sub(r"(\b)([Cc]a)n't", r"\1\2n not", text)
    text = re.sub(r"(\b)([Ii])'m", r"\1\2 am", text)
    text = re.sub(r"(\b)([Ll]et)'s", r"\1\2 us", text)
    text = re.sub(r"(\b)([Ww])on't", r"\1\2ill not", text)
    text = re.sub(r"(\b)([Ss])han't", r"\1\2hall not", text)
    text = re.sub(r"(\b)([Yy])(?:'all|a'll)", r"\1\2ou all", text)
    return text


def doc_ngrams(doc, n_from=1, n_to=2):
    return list(itertools.chain.from_iterable(
        [[doc[i:i + n] for i in range(len(doc) - (n - 1))]
         for n in range(n_from, n_to + 1)]))


def find_negations(doc, neg_comma=True, neg_modals=True, debug=False):
    """
    Takes as input a list of words and returns the positions (indices) of the words
    that are in the context of a negation.

    :param list doc: a list of words (strings)
    :param bool neg_comma: if True, the negation context ends on a comma
    :param bool neg_modals: if True, include negation modals in the set of negation words
    :param bool debug: if True, print the text color coded by context
    :return set: a set of the word positions inside a negation

    """
    doc_context = []
    append = doc_context.append
    negation_stopset = neg_puncts | {","} if neg_comma else set()
    negation_startset = negation_words | negation_modals if neg_modals else set()

    # status == "normal" means outside of parentheses
    # status == "parentheses" means inside parentheses
    # status[XXX] == True means that the context XXX is negated
    # status[XXX] == False means that the context XXX is affirmative
    status = {"normal": False, "parentheses": False}

    # pointer to the current context
    current = "normal"

    for i, tok in enumerate(doc):

        if tok in negation_startset:
            status[current] = True
            if debug:
                cprint(tok, 'red', attrs=['bold'], end=' ')
            continue

        if tok in negation_stopset | contrast_words:
            if debug:
                if status[current]:
                    cprint(tok, 'green', attrs=['bold'], end=' ')
                else:
                    print(tok, end=" ")
            status[current] = False
            continue

        if tok == "(":
            current = "parentheses"
            if debug:
                cprint(tok, 'green', attrs=['bold'], end=' ')
            continue

        if tok == ")":
            status[
                "parentheses"] = False  # in order to be false the next time it goes in to a parentheses
            current = "normal"
            if debug:
                cprint(tok, 'green', attrs=['bold'], end=' ')
            continue

        if debug:
            if status[current]:
                cprint(tok, 'magenta', end=' ')
            else:
                print(tok, end=" ")

        if status[current]:
            append(i)

    if debug:
        print()
    # input("press to continue...")

    return set(doc_context)


def mark_doc(doc, wids, mark=None, pos=None):
    """
    Given a list of words and a set of word positions, mark the words in those positions.
    :param list doc: a list of words (strings)
    :param set wids: the positions of the words to be marked
    :param string mark: a string that sets the mark that will be applied
                        to each of the selected words
    :param string pos: can be one of {"prefix", "suffix"}
    :return: the marked list of words
    """
    if mark is None:
        mark = "NEG"

    if pos is None:
        pos = "suffix"

    marked_doc = []

    for i, tok in enumerate(doc):
        if i in wids:
            if pos == "prefix":
                word = mark + "_" + tok
            else:
                word = tok + "_" + mark
            marked_doc.append(word)
        else:
            marked_doc.append(tok)

    return marked_doc


def polarity(doc, neg_comma=True, neg_modals=True):
    """
    Estimate the sentiment polarity of a tokenized document.
    Args:
        doc (): a list of words (strings)
        neg_comma (): if True, the negation context ends on a comma
        neg_modals (): if True, include negation modals in the set of negation words

    Returns:
        - polarity
        - [positive, negative, neutral] scores

    """

    tagged = nltk.pos_tag([wordnet_lemmatizer.lemmatize(w)
                           for w in doc])
    negations = find_negations(doc, neg_comma=neg_comma, neg_modals=neg_modals)
    scores = []
    for i, (word, tag) in enumerate(tagged):
        try:
            ss_set = None
            if 'NN' in tag and swn.senti_synsets(word):
                ss_set = list(swn.senti_synsets(word))[0]
            elif 'VB' in tag and swn.senti_synsets(word):
                ss_set = list(swn.senti_synsets(word))[0]
            elif 'JJ' in tag and swn.senti_synsets(word):
                ss_set = list(swn.senti_synsets(word))[0]
            elif 'RB' in tag and swn.senti_synsets(word):
                ss_set = list(swn.senti_synsets(word))[0]
            if ss_set:
                pos = ss_set.pos_score()
                neg = ss_set.neg_score()
                obj = ss_set.obj_score()
                if i in negations:
                    pos, neg = neg, pos
                scores.append([pos, neg, obj])
        except:
            pass

    _scores = numpy.mean(numpy.array(scores), axis=0)
    _polarity = _scores[0] - _scores[1]

    return _polarity, _scores
