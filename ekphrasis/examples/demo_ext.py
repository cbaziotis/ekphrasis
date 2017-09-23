"""
Created by Christos Baziotis.
"""
from ekphrasis.classes.tokenizer import SocialTokenizer


social_tokenizer = SocialTokenizer(lowercase=False).tokenize

sents = [
    "CANT WAIT for the new season of #TwinPeaks ＼(^o^)／ yaaaay!!! #davidlynch #tvseries :)))",
    "I saw the new #johndoe movie and it suuuuucks!!! WAISTED $10... #badmovies 3:/",
    "@SentimentSymp:  can't wait for the Nov 9 #Sentiment talks!  YAAAAAAY !!! >:-D http://sentimentsymposium.com/.",
]

for s in sents:
    print("SC : ", social_tokenizer(s))  # social tokenizer
