from ekphrasis.classes.segmenter import Segmenter

# segmenter using the word statistics from english Wikipedia
seg_eng = Segmenter(corpus="english")

# segmenter using the word statistics from Twitter
seg_tw = Segmenter(corpus="twitter")

words = ["exponentialbackoff", "gamedev", "retrogaming", "thewatercooler",
         "panpsychism"]
for w in words:
    print(w)
    print("(eng):", seg_eng.segment(w))
    print("(tw):", seg_tw.segment(w))
    print()
