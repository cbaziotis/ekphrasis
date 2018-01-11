"""
Created by Christos Baziotis.
"""
import nltk

from ekphrasis.classes.tokenizer import SocialTokenizer, Tokenizer


def wsp_tokenizer(text):
    return text.split(" ")


puncttok = nltk.WordPunctTokenizer().tokenize

social_tokenizer = SocialTokenizer(lowercase=False).tokenize
mytokenizer = Tokenizer(lowercase=False).tokenize

sents = [
    "CANT WAIT for the new season of #TwinPeaks ＼(^o^)／ yaaaay!!! #davidlynch #tvseries :)))",
    "@Calum5SOS You lil poop please follow @EmilyBain224 ☺️💕",
    "I saw the new #johndoe movie and it suuuuucks!!! WAISTED $10... #badmovies 3:/",
    "@SentimentSymp:  can't wait for the Nov 9 #Sentiment talks!  YAAAAAAY !!! >:-D http://sentimentsymposium.com/.",
]

for s in sents[:3]:
    print()
    # print("ORG: ", s)  # original sentence
    # print("WSP : ", wsp_tokenizer(s))  # whitespace tokenizer
    # print("WPU : ", puncttok(s))  # WordPunct tokenizer
    # print("SC : ", social_tokenizer(s))  # social tokenizer
    print("SC : ", mytokenizer(s))  # social tokenizer
