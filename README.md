Collection of lightweight text tools, geared towards text from social networks, such as Twitter or Facebook, for tokenization, word normalization, word segmentation (for splitting hashtags) and spell correction, 
using word statistics from 2 big corpora (english Wikipedia, twitter - 330mil english tweets).

_ekphrasis_ was developed as part of the text processing pipeline for
_DataStories_ team's submission for _SemEval-2017 Task 4 (English), Sentiment Analysis in Twitter_.

If you use the library in you research project, please cite the paper 
["DataStories at SemEval-2017 Task 4: Deep LSTM with Attention for Message-level and Topic-based Sentiment Analysis"](http://www.aclweb.org/anthology/S17-2126).

Citation:
```
@InProceedings{baziotis-pelekis-doulkeridis:2017:SemEval2,
  author    = {Baziotis, Christos  and  Pelekis, Nikos  and  Doulkeridis, Christos},
  title     = {DataStories at SemEval-2017 Task 4: Deep LSTM with Attention for Message-level and Topic-based Sentiment Analysis},
  booktitle = {Proceedings of the 11th International Workshop on Semantic Evaluation (SemEval-2017)},
  month     = {August},
  year      = {2017},
  address   = {Vancouver, Canada},
  publisher = {Association for Computational Linguistics},
  pages     = {747--754}
}
```

**Disclaimer:** The library is no longer actively developed. I will try to resolve important issues, but I can't make any promises.

# Installation

build from source 
```
pip install git+git://github.com/cbaziotis/ekphrasis.git
```
or install from pypi
```
pip install ekphrasis -U
```

# Overview

_ekphrasis_ offers the following functionality:

  1. **Social Tokenizer**. A text tokenizer geared towards social networks (Facebook, Twitter...), 
      which understands complex emoticons, emojis and other unstructured expressions like dates, times and more.

  2. **Word Segmentation**. You can split a long string to its constituent words. Suitable for hashtag segmentation.

  3. **Spell Correction**. You can replace a misspelled word, with the most probable candidate word.

  4. **Customization**. Taylor the word-segmentation, spell-correction and term identification, to suit your needs.
  
      Word Segmentation and Spell Correction mechanisms, operate on top of word statistics, collected from a given corpus. We provide word statistics from 2 big corpora (from Wikipedia and Twitter), but you can also generate word statistics from your own corpus. You may need to do that if you are working with domain-specific texts, like biomedical documents. For example a word describing a technique or a chemical compound may be treated as a misspelled word, using the word statistics from a general purposed corpus.

      _ekphrasis_ tokenizes the text based on a list of regular expressions. You can easily enable _ekphrasis_ to identify new entities, by simply adding a new entry to the dictionary of regular expressions (`ekphrasis/regexes/expressions.txt`).

  5. **Pre-Processing Pipeline**. You can combine all the above steps in an easy way, in order to prepare the text files in your dataset for some kind of analysis or for machine learning.
  In addition, to the aforementioned actions, you can perform text normalization, word annotation (labeling) and more.




## Text Pre-Processing pipeline

You can easily define a preprocessing pipeline, by using the ``TextPreProcessor``. 

```python
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons

text_processor = TextPreProcessor(
    # terms that will be normalized
    normalize=['url', 'email', 'percent', 'money', 'phone', 'user',
        'time', 'url', 'date', 'number'],
    # terms that will be annotated
    annotate={"hashtag", "allcaps", "elongated", "repeated",
        'emphasis', 'censored'},
    fix_html=True,  # fix HTML tokens
    
    # corpus from which the word statistics are going to be used 
    # for word segmentation 
    segmenter="twitter", 
    
    # corpus from which the word statistics are going to be used 
    # for spell correction
    corrector="twitter", 
    
    unpack_hashtags=True,  # perform word segmentation on hashtags
    unpack_contractions=True,  # Unpack contractions (can't -> can not)
    spell_correct_elong=False,  # spell correction for elongated words
    
    # select a tokenizer. You can use SocialTokenizer, or pass your own
    # the tokenizer, should take as input a string and return a list of tokens
    tokenizer=SocialTokenizer(lowercase=True).tokenize,
    
    # list of dictionaries, for replacing tokens extracted from the text,
    # with other expressions. You can pass more than one dictionaries.
    dicts=[emoticons]
)

sentences = [
    "CANT WAIT for the new season of #TwinPeaks ＼(^o^)／!!! #davidlynch #tvseries :)))",
    "I saw the new #johndoe movie and it suuuuucks!!! WAISTED $10... #badmovies :/",
    "@SentimentSymp:  can't wait for the Nov 9 #Sentiment talks!  YAAAAAAY !!! :-D http://sentimentsymposium.com/."
]

for s in sentences:
    print(" ".join(text_processor.pre_process_doc(s)))
```

Output:

```
cant <allcaps> wait <allcaps> for the new season of <hashtag> twin peaks </hashtag> ＼(^o^)／ ! <repeated> <hashtag> david lynch </hashtag> <hashtag> tv series </hashtag> <happy>

i saw the new <hashtag> john doe </hashtag> movie and it sucks <elongated> ! <repeated> waisted <allcaps> <money> . <repeated> <hashtag> bad movies </hashtag> <annoyed>

<user> : can not wait for the <date> <hashtag> sentiment </hashtag> talks ! yay <allcaps> <elongated> ! <repeated> <laugh> <url>
```


Notes:

* elongated words are automatically normalized.
* Spell correction affects performance.

---

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

words = ["exponentialbackoff", "gamedev", "retrogaming", "thewatercooler", "panpsychism"]
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

panpsychism
(eng): panpsychism
(tw): pan psych is m

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
our tokenizer is able to identify almost all emoticons, emojis and many complex expressions.

Especially for tasks such as sentiment analysis, there are many expressions that play a decisive role in identifying the sentiment expressed in text. Expressions like these are: 

- Censored words, such as ``f**k``, ``s**t``.
- Words with emphasis, such as ``a *great* time``, ``I don't *think* I ...``.
- Emoticons, such as ``>:(``, ``:))``, ``\o/``.
- Dash-separated words, such as ``over-consumption``, ``anti-american``, ``mind-blowing``.

Moreover, ekphrasis can identify information-bearing  expressions. Depending on the task, you may want to keep preserve / extract them as one token (IR) and then normalize them since this information may be irrelevant for the task (sentiment analysis). Expressions like these are:


-   Dates, such as ``Feb 18th``, ``December 2, 2016``, ``December 2-2016``,
    ``10/17/94``, ``3 December 2016``, ``April 25, 1995``, ``11.15.16``,
    ``November 24th 2016``, ``January 21st``.
-   Times, such as ``5:45pm``, ``11:36 AM``, ``2:45 pm``, ``5:30``.
-   Currencies, such as ``$220M``, ``$2B``, ``$65.000``, ``€10``, ``$50K``.
-   Phone numbers.
-   URLs, such as ``http://www.cs.unipi.gr``, ``https://t.co/Wfw5Z1iSEt``.

**Example**:

```python
import nltk
from ekphrasis.classes.tokenizer import SocialTokenizer


def wsp_tokenizer(text):
    return text.split(" ")

puncttok = nltk.WordPunctTokenizer().tokenize

social_tokenizer = SocialTokenizer(lowercase=False).tokenize

sents = [
    "CANT WAIT for the new season of #TwinPeaks ＼(^o^)／ yaaaay!!! #davidlynch #tvseries :)))",
    "I saw the new #johndoe movie and it suuuuucks!!! WAISTED $10... #badmovies >3:/",
    "@SentimentSymp:  can't wait for the Nov 9 #Sentiment talks!  YAAAAAAY !!! >:-D http://sentimentsymposium.com/.",
]

for s in sents:
    print()
    print("ORG: ", s)  # original sentence
    print("WSP : ", wsp_tokenizer(s))  # whitespace tokenizer
    print("WPU : ", puncttok(s))  # WordPunct tokenizer
    print("SC : ", social_tokenizer(s))  # social tokenizer

```

Output:

```
ORG:  CANT WAIT for the new season of #TwinPeaks ＼(^o^)／ yaaaay!!! #davidlynch #tvseries :)))
WSP :  ['CANT', 'WAIT', 'for', 'the', 'new', 'season', 'of', '#TwinPeaks', '＼(^o^)／', 'yaaaay!!!', '#davidlynch', '#tvseries', ':)))']
WPU :  ['CANT', 'WAIT', 'for', 'the', 'new', 'season', 'of', '#', 'TwinPeaks', '＼(^', 'o', '^)／', 'yaaaay', '!!!', '#', 'davidlynch', '#', 'tvseries', ':)))']
SC :  ['CANT', 'WAIT', 'for', 'the', 'new', 'season', 'of', '#TwinPeaks', '＼(^o^)／', 'yaaaay', '!', '!', '!', '#davidlynch', '#tvseries', ':)))']

ORG:  I saw the new #johndoe movie and it suuuuucks!!! WAISTED $10... #badmovies >3:/
WSP :  ['I', 'saw', 'the', 'new', '#johndoe', 'movie', 'and', 'it', 'suuuuucks!!!', 'WAISTED', '$10...', '#badmovies', '>3:/']
WPU :  ['I', 'saw', 'the', 'new', '#', 'johndoe', 'movie', 'and', 'it', 'suuuuucks', '!!!', 'WAISTED', '$', '10', '...', '#', 'badmovies', '>', '3', ':/']
SC :  ['I', 'saw', 'the', 'new', '#johndoe', 'movie', 'and', 'it', 'suuuuucks', '!', '!', '!', 'WAISTED', '$10', '.', '.', '.', '#badmovies', '>', '3:/']
```



<!-- 

---
_Ekphrasis_ means expression in Greek (Modern Greek:έκφραση, Ancient Greek:ἔκφρασις). 
 relies on Regular Expression for the text tokenization.

 -->

#### References

[1] K. Gimpel et al., “Part-of-speech tagging for twitter: Annotation, features, and experiments,” in Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies: short papers-Volume 2, 2011, pp. 42–47.

[2] C. Potts, “Sentiment Symposium Tutorial: Tokenizing,” Sentiment Symposium Tutorial, 2011. [Online]. Available: http://sentiment.christopherpotts.net/tokenizing.html.
