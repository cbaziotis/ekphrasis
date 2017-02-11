from classes.SocialTokenizer import SocialTokenizer
from classes.TextPreProcessor import TextPreProcessor
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
    dicts=[emoticons])

sentences = [
    "CANT WAIT for the new season of #TwinPeaks ＼(^o^)／ !!! #DavidLynch #tvseries :) ",
    "The new #johndoe suuuuucks!!! WAISTED $10... #badmovies >:/",
    "Sophos aims to raise $100m in London IPO",
    "When there are no words , use emojis 😎",
    "The sound of #Sunday with Bee Gees - Alive https://t.co/CvHFOMO1tN #webradio #internetradio",
    "I hope Paul Dunne blows up tomorrow only because UAB beats us in the tourney... #stillnotoverit",
    "It's National Ice Cream Day on Sunday, July 19. Get the ice cream scoop.  http://t.co/S6yXXQHzHk #nationalicecreamday",
    "Watchman may have drowned on the job  On 16.07.15, at 9:11 p.m., police responded to a report of a watchman found... http://t.co/UdEXjQFeqq",
    "The Week in Ransomware - December 16th 2016 - Samas, No More Ransom, Screen Lockers, and More https://t.co/MWgeYhnMk7 #technology https://t.co/Wzb1qoU6cG",
    "#FantasticBeasts is an excellent movie, in my opinion, but I still can't wait for @cinemasins to sin the sh*t out of it",
    "Not sure how I feel about the Black Keys playing at the U-Village Microsoft store. Guess they *are* getting paid, that's good. #Microsoft",
    "Good night #Twitter and #TheLegionoftheFallen.  5:45am cimes awfully early!",
]

for s in sentences:
    print()
    print(s)
    print(" ".join(text_processor.pre_process_doc(s)))
