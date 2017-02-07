import html
import re

import colorama
from termcolor import colored

from classes.expressions import Expressions


class SocialTokenizer:
    def __init__(self, lowercase=False, verbose=False, debug=False, **kwargs):
        self.lowercase = lowercase
        self.debug = debug
        self.verbose = verbose
        colorama.init(autoreset=False, convert=False, strip=False, wrap=True)
        pipeline = []
        self.regexes = Expressions().EXPRESSIONS

        emojis = kwargs.get("emojis", True)
        urls = kwargs.get("urls", True)
        tags = kwargs.get("tags", True)
        emails = kwargs.get("emails", True)
        users = kwargs.get("users", True)
        hashtags = kwargs.get("hashtags", True)
        cashtags = kwargs.get("cashtags", True)
        phones = kwargs.get("phones", True)
        percents = kwargs.get("percents", True)
        money = kwargs.get("money", True)
        date = kwargs.get("date", True)
        time = kwargs.get("time", True)
        acronyms = kwargs.get("acronyms", True)
        emoticons = kwargs.get("emoticons", True)
        censored = kwargs.get("censored", True)
        emphasis = kwargs.get("emphasis", True)
        numbers = kwargs.get("numbers", True)

        if emojis:
            try:
                re.compile(self.regexes["EMOJI_UCS4"])
                pipeline.append(self.regexes["EMOJI_UCS4"])
            except re.error:
                re.compile(self.regexes["EMOJI_UCS2"])
                pipeline.append(self.regexes["EMOJI_UCS2"])

        if urls:
            pipeline.append(self.regexes["URL"])

        if tags:
            pipeline.append(self.regexes["TAG"])

        if emails:
            pipeline.append(self.wrap_non_matching(self.regexes["EMAIL"]))

        if users:
            pipeline.append(self.wrap_non_matching(self.regexes["USER"]))

        if hashtags:
            pipeline.append(self.wrap_non_matching(self.regexes["HASHTAG"]))

        if cashtags:
            pipeline.append(self.wrap_non_matching(self.regexes["CASHTAG"]))

        if phones:
            pipeline.append(self.wrap_non_matching(self.regexes["PHONE"]))

        if percents:
            pipeline.append(self.wrap_non_matching(self.regexes["PERCENT"]))

        if money:
            pipeline.append(self.wrap_non_matching(self.regexes["MONEY"]))

        if date:
            pipeline.append(self.wrap_non_matching(self.regexes["DATE"]))

        if time:
            pipeline.append(self.wrap_non_matching(self.regexes["TIME"]))

        if acronyms:
            pipeline.append(self.wrap_non_matching(self.regexes["ACRONYM"]))

        if emoticons:
            pipeline.append(self.regexes["LTR_FACE"])
            pipeline.append(self.regexes["RTL_FACE"])

        if censored:
            pipeline.append(self.wrap_non_matching(self.regexes["CENSORED"]))

        if emphasis:
            pipeline.append(self.wrap_non_matching(self.regexes["EMPHASIS"]))

        # terms like 'eco-friendly', 'go_to', 'john's' - maybe remove the ' or add a parameter for it
        # pipeline.append(r"(?:\b[a-zA-Z]+[a-zA-Z'\-_]+[a-zA-Z]+\b)")

        # <3 ^5
        if emoticons:
            pipeline.append(self.wrap_non_matching(self.regexes["REST_EMOTICONS"]))

        if numbers:
            pipeline.append(self.regexes["NUMBER"])

        # any other word
        pipeline.append(r"(?:[\w_]+)")

        # EASTERN EMOTICONS - (^_^;)   (>_<)>  ＼(^o^)／
        if emoticons:
            pipeline.append(self.wrap_non_matching(self.regexes["EASTERN_EMOTICONS"]))

        # keep repeated puncts as one term
        # pipeline.append(r"")

        pipeline.append("(?:\S)")  # CATCH ALL remaining terms

        self.tok = re.compile(r"({})".format("|".join(pipeline)))

    @staticmethod
    def wrap_non_matching(exp):
        return "(?:{})".format(exp)

    def verbose_text(self, text, tokenized):
        # print(text.rstrip())
        for term in tokenized:
            print(colored(term, 'red', attrs=["underline"]), end=" ")
        print()
        if self.debug:
            input()
        else:
            print()

    def tokenize(self, text):
        escaped = html.unescape(text)
        tokenized = self.tok.findall(escaped)

        if self.verbose:
            self.verbose_text(text, tokenized)

        if self.lowercase:
            tokenized = [t.lower() for t in tokenized]

        return tokenized


sentences = []

# [print(s) for s in sentences]
# tokenizer = SocialTokenizer(debug=True, verbose=True)
#
# for s in sentences:
#     tokenizer.tokenize(s)
