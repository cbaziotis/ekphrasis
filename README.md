Text processing tool, geared towards text from social networks, such as Twitter or Facebook.
The tool performs tokenization, word normalization, word segmentation (for splitting hashtags) and spell correction, 
using word statistics from 2 big corpora (english Wikipedia, twitter - 330mil english tweets).

_ekphrasis_ was developed as part of the text processing pipeline for
_DataStories_ team's submission for _SemEval-2017 Task 4 (English), Sentiment Analysis in Twitter_.

**Documentation and complete examples will be coming soon.**


## Overview

_ekphrasis_ processes text in two steps: 
  1. **Tokenization**. The difficulty in tokenization is to avoid splitting expressions or words that should be kept intact (as one token).
  Although there are some tokenizers geared towards Twitter [1],[2] that recognize the Twitter markup 
  and some basic sentiment expressions or simple emoticons. 
  Our tokenizer offers additional functionality as it is able to identify most emoticons, emojis, expressions such as 
  dates (e.g. 07/11/2011, April 23rd), times (e.g. 4:30pm, 11:00 am), currencies (e.g. \$10, 25mil, 50€), acronyms, censored words (e.g. s**t), 
  words with emphasis (e.g. *very*) and more.
 
  2. **Post-processing**. After the tokenization you can perform an extra postprocessing step, applying modifications on the extracted tokens.
  This is where you can perform spell correction, word normalization and segmentation and decide which tokens to omit, normalize or annotate (surround or replace with special tags).




### Word Statistics
_ekphrasis_ provides word statistics (unigrams and bigrams) from 2 big corpora:
* the english Wikipedia
* a collection of 330 million english Twitter messages

These word statistics are required for the word segmentation and spell correction.
Moreover, you can generate word statistics from your own corpus.
You can use `ekphrasis/tools/generate_stats.py` and generate statistics from a text file, or a directory that contains a collection of text files.
For example, in order generate word statistics for [text8](http://mattmahoney.net/dc/textdata.html) (http://mattmahoney.net/dc/text8.zip), you can do:
 
```python
python generate_stats.py --input text8.txt --name text8 --ngrams 2 --mincount 70 30
```
* input: path to file or directory containing the files for calculating the statistics.
* name: the name of the corpus.
* ngrams: up-to how many ngrams to calculate statistics.
* mincount: the minimum count of each ngram, in order to be included. 
In this case, the mincount for unigrams is 70 and for bigrams is 30.

After you run the script, you will see a new directory inside `ekphrasis/stats/` with the statistics of your corpus. 
In the case of the example above, `ekphrasis/stats/text8/`. 



### Word Segmentation
The word segmentation implementation uses the Viterbi algorithm and is based on [CH14](http://norvig.com/ngrams/ch14.pdf) from the book [Beautiful Data (Segaran and Hammerbacher, 2009)](http://shop.oreilly.com/product/9780596157128.do).
The implementation requires word statistics in order to identify and separating the words in a string. 
You can use the word statistics from one of the 2 provided corpora, or from your own corpus.


**Example:**
In order to perform word segmentation, first you have to instantiate a segmenter with a given corpus, and then just use the `segment()` method:
```python
seg = Segmenter(corpus="mycorpus") 
print(seg.segment("smallandinsignificant"))
```
```
> small and insignificant
```

You can test the output using statistics from the different corpora:
```python
from ekphrasis.classes.segmenter import Segmenter

# segmenter using the word statistics from english Wikipedia
seg_eng = Segmenter(corpus="english") 

# segmenter using the word statistics from Twitter
seg_tw = Segmenter(corpus="twitter")

words = ["insufficientnumbers", "exponentialbackoff", "sitdown", "gamedev", "retrogaming","thewatercooler", "homonculus"]
for w in words:
    print(w)
    print("(eng):", seg_eng.segment(w))
    print("(tw):", seg_tw.segment(w))
    print()
```
Output:
```
insufficientnumbers
(eng): insufficient numbers
(tw): insufficient numbers

exponentialbackoff
(eng): exponential backoff
(tw): exponential back off

sitdown
(eng): sit down
(tw): sit down

gamedev
(eng): gamedev
(tw): game dev

retrogaming
(eng): retrogaming
(tw): retro gaming

thewatercooler
(eng): the water cooler
(tw): the watercooler

homonculus
(eng): homonculus
(tw): ho mon cul us

```


### Spell Correction
The Spell Corrector extends the functionality of Peter Norvig's spell-corrector.



---
_Ekphrasis_ means expression in Greek (Modern Greek:έκφραση, Ancient Greek:ἔκφρασις). 
 <!--relies on Regular Expression for the text tokenization.-->

#### References

[1] K. Gimpel et al., “Part-of-speech tagging for twitter: Annotation, features, and experiments,” in Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies: short papers-Volume 2, 2011, pp. 42–47.

[2] C. Potts, “Sentiment Symposium Tutorial: Tokenizing,” Sentiment Symposium Tutorial, 2011. [Online]. Available: http://sentiment.christopherpotts.net/tokenizing.html.
