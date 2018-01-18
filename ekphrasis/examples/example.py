from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons


def ws_tokenizer(text):
    return text.split()


text_processor = TextPreProcessor(
    normalize=['url', 'email', 'percent', 'money', 'phone', 'user', 'time',
               'date', 'number'],
    annotate={"hashtag", "elongated", "allcaps", "repeated", 'emphasis',
              'censored'},
    all_caps_tag="wrap",
    fix_text=True,
    segmenter="twitter_2018",
    corrector="twitter_2018",
    unpack_hashtags=True,
    unpack_contractions=True,
    spell_correct_elong=False,
    tokenizer=SocialTokenizer(lowercase=True).tokenize,
    # tokenizer=ws_tokenizer,
    dicts=[emoticons]
)

sentences = [
    "CANT WAIT for the new season of #TwinPeaks ＼(^o^)／!!! #davidlynch #tvseries :))) ",
    "I saw the new #johndoe movie and it suuuuucks!!! WAISTED $10... #badmovies :/",
    "I saw the new #JOHNDOE movie AND IT SUCKS!!! WAISTED $10... #badmovies :/",
    "@SentimentSymp:  can't wait for the Nov 9 #Sentiment talks!  YAAAAAAY !!! :-D http://sentimentsymposium.com/.",
    "Thanks x https://t.co/ZXTcDLyDS9",
    "@Calum5SOS You lil poop please follow @EmilyBain224 ☺️💕",
    "Words attendees would use to describe @prosper4africa's #ALN2015! https://t.co/hmNm8AdwOh",
]

for s in sentences:
    print()
    print(s)
    print(" ".join(text_processor.pre_process_doc(s)))
