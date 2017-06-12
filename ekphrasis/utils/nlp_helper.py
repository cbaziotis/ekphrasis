import itertools
import re

from termcolor import cprint

# additional negations: nowhere
negation_words = {"'t", "ain't", 'aint', "aren't", 'arent', 'cant',
                  "didn't", 'didnt', "doesn't", 'doesnt', "don't", 'dont',
                  "hadn't", 'hadnt', "hasn't", 'hasnt', "haven't", 'havent', "isn't", 'isnt',
                  'never', 'no', 'none', 'noone', 'not', 'nothing', 'wont', }
negation_modals = {"couldn't", 'couldnt', "shouldn't", 'shouldnt', "wouldn't", 'wouldnt'}
contrast_words = {"but", "although", "though", "however", "despite", "whereas", "while", "unlike", "still"}
neg_puncts = {"\n", ".", "?", ":", "..."}

# [print(word,", ") for word in negation_words | negation_modals]


NE_entities = {"PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE"}
NE_quantities = {"DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"}

REGEX_HASHTAG = re.compile(r"#\w*", re.IGNORECASE)
REGEX_MENTION = re.compile(r"@\w*", re.IGNORECASE)
REGEX_ELONG = re.compile(r"([a-zA-Z])\1{2,}", re.IGNORECASE)
REGEX_EMOTICON = re.compile(r"(?::|;|=)(?:-)?(?:\)|\(|D|P)", re.UNICODE)
REGEX_NPUNCTS = re.compile(r"[!?]{2,}", re.UNICODE)
REGEX_QUOTES = re.compile(r"\"(\\.|[^\"]){2,}\"", re.UNICODE)


def text_has_emoticon(text):
    return REGEX_EMOTICON.search(text)


def text_has_continuous_puncts(text):
    return REGEX_NPUNCTS.search(text)


def text_has_elong(text):
    return REGEX_LOOONG.search(text)


def text_has_quotes(text):
    return REGEX_QUOTES.search(text)


def doc_ngrams(doc, n_from=1, n_to=2):
    return list(itertools.chain.from_iterable([[doc[i:i + n] for i in range(len(doc) - (n - 1))]
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
            status["parentheses"] = False  # in order to be false the next time it goes in to a parentheses
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
