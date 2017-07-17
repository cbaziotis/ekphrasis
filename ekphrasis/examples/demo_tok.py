"""
Created by Christos Baziotis.
"""
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.examples.demo_data import demo_sents


def ws_tokenizer(text):
    return text.split()


social_tokenizer = SocialTokenizer(lowercase=False).tokenize

for s in demo_sents:
    print()
    print("ORG: ", s)  # original sentence
    print("WP : ", ws_tokenizer(s))  # whitespace tokenizer
    print("SC : ", social_tokenizer(s))  # social tokenizer
