import re
from collections import Counter
from difflib import SequenceMatcher
from functools import lru_cache

from ekphrasis.utils.helpers import read_stats

REGEX_TOKEN = re.compile(r'\b[a-z]{2,}\b')


class SpellCorrector:
    """
    The SpellCorrector extends the functionality of the Peter Norvig's
    spell-corrector in http://norvig.com/spell-correct.html
    """

    def __init__(self, corpus="english"):
        """

        :param corpus: the statistics from which corpus to use for the spell correction.
        """
        super().__init__()
        self.WORDS = Counter(read_stats(corpus, 1))
        self.N = sum(self.WORDS.values())

    @staticmethod
    def tokens(text):
        return REGEX_TOKEN.findall(text.lower())

    def P(self, word):
        """
        Probability of `word`.
        """
        return self.WORDS[word] / self.N

    def most_probable(self, words):
        _known = self.known(words)
        if _known:
            return max(_known, key=self.P)
        else:
            return []

    @staticmethod
    def edit_step(word):
        """
        All edits that are one edit away from `word`.
        """
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        """
        All edits that are two edits away from `word`.
        """
        return (e2 for e1 in self.edit_step(word)
                for e2 in self.edit_step(e1))

    def known(self, words):
        """
        The subset of `words` that appear in the dictionary of WORDS.
        """
        return set(w for w in words if w in self.WORDS)

    @staticmethod
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def edit_candidates(self, word, assume_wrong=False, fast=True):
        """
        Generate possible spelling corrections for word.
        """

        if fast:
            if assume_wrong:
                return self.known(self.edit_step(word)) or [word]
            else:
                return self.known([word]) or self.known(self.edit_step(word)) or [word]
        else:
            if assume_wrong:
                ttt = self.known(self.edit_step(word)) or self.known(self.edits2(word)) or {word}
                return ttt
            else:
                return self.known([word]) or self.known(self.edit_step(word)) or self.known(self.edits2(word)) or [word]

    # def distance_candidates(self, word, max_distance=3):
    #     """
    #     Generate possible spelling corrections for word.
    #     """
    #     candidates = [w for w in self.WORDS if w]
    #     return self.known([word]) or self.known(self.edit_step(word)) or self.known(self.edits2(word)) or [word]

    @lru_cache(maxsize=65536)
    def correct(self, word, assume_wrong=False, fast=False):
        """
        Most probable spelling correction for word.
        """
        return max(self.edit_candidates(word, assume_wrong=assume_wrong, fast=fast), key=self.P)

    def correct_text(self, text):
        """
        Correct all the words within a text, returning the corrected text."""

        return re.sub('[a-zA-Z]+', self.correct_match, text)

    def correct_match(self, match):
        """
        Spell-correct word in match, and preserve proper upper/lower/title case.
        """

        word = match.group()
        return self.case_of(word)(self.correct(word.lower()))

    def correct_word(self, word, assume_wrong=False, fast=False):
        """
        Spell-correct word in match, and preserve proper upper/lower/title case.
        """

        return self.case_of(word)(self.correct(word.lower(), assume_wrong=assume_wrong, fast=fast))

    @staticmethod
    def case_of(text):
        """
        Return the case-function appropriate for text: upper, lower, title, or just str.
        """

        return (str.upper if text.isupper() else
                str.lower if text.islower() else
                str.title if text.istitle() else
                str)

    def elong_normalized_candidates(self, word, acc=None):
        if acc is None:
            acc = []
        candidates = [w for w in set(word) if word.count(w) > 1]
        for c in candidates:
            _w = word.replace(c + c, c)
            if _w in acc:
                continue
            acc.append(_w)
            self.elong_normalized_candidates(_w, acc)
        return acc + [word]

    def best_elong_candidate(self, word):
        candidates = self.elong_normalized_candidates(word)
        best = self.most_probable(candidates)
        return best or word

    def normalize_elongated(self, word):
        return self.case_of(word)(self.best_elong_candidate(word.lower()))
