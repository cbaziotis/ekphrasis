from ekphrasis.classes.segmenter import Segmenter

# segmenter using the word statistics from english Wikipedia
seg_eng = Segmenter(corpus="english")

# segmenter using the word statistics from Twitter
seg_tw = Segmenter(corpus="twitter")

# segmenter using the word statistics from Twitter
seg_tw_2018 = Segmenter(corpus="twitter_2018")

words = ["exponentialbackoff", "gamedev", "retrogaming", "thewatercooler",
         "panpsychism"]
for w in words:
    print(w)
    print("(eng):", seg_eng.segment(w))
    print("(tw):", seg_tw.segment(w))
    print("(tw):", seg_tw_2018.segment(w))
    print()
