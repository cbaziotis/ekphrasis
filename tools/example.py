from classes.textpp import TextPreProcessor
from classes.tokenizer import SocialTokenizer
from dicts.emoticons import emoticons

text_processor = TextPreProcessor(
    backoff=['url', 'email', 'percent', 'money', 'phone', 'user', 'time', 'url', 'date', 'number'],
    include_tags={"hashtag", "allcaps", "elongated", "repeated", 'emphasis', 'censored'},
    fix_html=True,
    segmenter="twitter",
    corrector="twitter",
    unpack_hashtags=True,
    unpack_contractions=True,
    spell_correct_elong=False,
    tokenizer=SocialTokenizer(lowercase=True).tokenize,
    dicts=[emoticons]
)

sentences = [
    "CANT WAIT for the new season of #TwinPeaks ＼(^o^)／ !!! #davidlynch #tvseries :))) ",
    "The *new* season of #TwinPeaks is coming May 21, 2017. CANT WAIT \o/!!! #tvseries #davidlynch :D",
    "I saw the new #johndoe movie and it suuuuucks!!! WAISTED $10... #badmovies >:/",
    "@SentimentSymp:  can't wait for the Nov 9 #Sentiment talks!  YAAAAAAY !!! >:-D http://sentimentsymposium.com/.",
]

for s in sentences:
    print()
    print(s)
    print(" ".join(text_processor.pre_process_doc(s)))
