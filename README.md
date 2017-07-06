Collection of lightweight text processing tools, geared towards text from social networks, such as Twitter or Facebook.
The tool performs tokenization, word normalization, word segmentation (for splitting hashtags) and spell correction, 
using word statistics from 2 big corpora (english Wikipedia, twitter - 330mil english tweets).

_ekphrasis_ was developed as part of the text processing pipeline for
_DataStories_ team's submission for _SemEval-2017 Task 4 (English), Sentiment Analysis in Twitter_.

Note: 
More examples will be coming soon...

## Installation
```
pip install ekphrasis
```


## Overview

_ekphrasis_ offers the following functionality:
 
  1. **Social Tokenizer**. A text tokenizer geared towards social networks (Facebook, Twitter...), 
  which understands complex emoticons, emojis and other unstructured expressions like dates, times and more.
  
  2. **Word Segmentation**. You can split a long string to its constituent words. Suitable for hashtag segmentation.
 
  3. **Spell Correction**. You can replace a misspelled word, with the most probable candidate word.
  
  3. **Customization**. Word Segmentation and Spell Correction mechanisms, operate on top of word statistics, collected from a given corpus.
  We provide word statistics from 2 big corpora (from Wikipedia and Twitter), but you can also generate word statistics from your own corpus.
  You may need to do that if you are working with domain-specific texts, like biomedical documents. 
  For example a word describing a technique or a chemical compound may be treated as a misspelled word, using the word statistics from a general purposed corpus.
  
  4. **PreProcessing Pipeline**. You can combine all the above steps in an easy way, 
  in order to prepare the text files in your dataset for some kind of analysis or for machine learning.
  In addition, to the aforementioned actions, you can perform text normalization, word annotation (labeling) and more.




### Word Statistics
_ekphrasis_ provides word statistics (unigrams and bigrams) from 2 big corpora:
* the english Wikipedia
* a collection of 330 million english Twitter messages

These word statistics are required for the word segmentation and spell correction.
Moreover, you can generate word statistics from your own corpus.
You can use `ekphrasis/tools/generate_stats.py` and generate statistics from a text file, or a directory that contains a collection of text files.
For example, in order generate word statistics for [text8](http://mattmahoney.net/dc/textdata.html) (http://mattmahoney.net/dc/text8.zip), you can do:
 
```
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
from ekphrasis.classes.segmenter import Segmenter
seg = Segmenter(corpus="mycorpus") 
print(seg.segment("smallandinsignificant"))
```
Output:
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

words = ["exponentialbackoff", "gamedev", "retrogaming", "thewatercooler", "homonculus"]
for w in words:
    print(w)
    print("(eng):", seg_eng.segment(w))
    print("(tw):", seg_tw.segment(w))
    print()
```
Output:
```
exponentialbackoff
(eng): exponential backoff
(tw): exponential back off

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

Finally, if the word is camelCased or PascalCased, then the algorithm splits the words based on the case of the characters.
```python
from ekphrasis.classes.segmenter import Segmenter
seg = Segmenter() 
print(seg.segment("camelCased"))
print(seg.segment("PascalCased"))
```
Output:
```
> camel cased
> pascal cased
```

### Spell Correction
The Spell Corrector is based on [Peter Norvig's spell-corrector](http://norvig.com/spell-correct.html).
Just like the segmentation algorithm, we utilize word statistics in order to find the most probable candidate.
Besides the provided statistics, you can use your own.

**Example:**

You can perform the spell correction, just like the word segmentation.
First you have to instantiate a `SpellCorrector` object, 
that uses the statistics from the corpus of your choice and then use on of the available methods.
```python
from ekphrasis.classes.spellcorrect import SpellCorrector
sp = SpellCorrector(corpus="english") 
print(sp.correct("korrect"))
```
Output:
```
> correct
```


### Social Tokenizer
The difficulty in tokenization is to avoid splitting expressions or words that should be kept intact (as one token).
This is more important in texts from social networks, with "creative" writing and expressions like emoticons, hashtags and so on.
Although there are some tokenizers geared towards Twitter [1],[2], 
that recognize the Twitter markup and some basic sentiment expressions or simple emoticons, 
our tokenizer is able to identify almost all emoticons, emojis, expressions such 
as dates (e.g. 07/11/2011, April 23rd), times (e.g. 4:30pm, 11:00 am), 
currencies (e.g. \$10, 25mil, 50\euro), acronyms, censored words (e.g. s**t), 
words with emphasis (e.g. *very*) and more.


<!-- 

---
_Ekphrasis_ means expression in Greek (Modern Greek:έκφραση, Ancient Greek:ἔκφρασις). 
 relies on Regular Expression for the text tokenization.
 
 -->

#### References

[1] K. Gimpel et al., “Part-of-speech tagging for twitter: Annotation, features, and experiments,” in Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies: short papers-Volume 2, 2011, pp. 42–47.

[2] C. Potts, “Sentiment Symposium Tutorial: Tokenizing,” Sentiment Symposium Tutorial, 2011. [Online]. Available: http://sentiment.christopherpotts.net/tokenizing.html.
