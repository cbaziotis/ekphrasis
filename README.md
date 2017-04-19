Text processing tool, geared towards text from social networks, such as Twitter or Facebook.
The tool performs tokenization, word normalization, word segmentation (for splitting hashtags) and spell correction, 
using word statistics from 2 big corpora (english Wikipedia, twitter - 330mil english tweets).

_ekphrasis_ was developed as part of the text processing pipeline for
_DataStories_ team's systems for _SemEval-2017 Task 4 (English), Sentiment Analysis in Twitter_.

**Documentation and complete examples will be coming soon.**

## Overview

_ekphrasis_ processes text in two steps: 
  1. **Tokenization**. The difficulty in tokenization is to avoid splitting expressions or words that should be kept intact (as one token).
  Although there are some tokenizers geared towards Twitter [1],[2] that recognize the Twitter markup 
  and some basic sentiment expressions or simple emoticons. 
  Our tokenizer offers additional functionality as it is able to identify most emoticons, emojis, expressions such as 
  dates (e.g. 07/11/2011, April 23rd), times (e.g. 4:30pm, 11:00 am), currencies (e.g. \$10, 25mil, 50\euro), acronyms, censored words (e.g. s**t), 
  words with emphasis (e.g. *very*) and more.
 
  2. **Post-processing**. After the tokenization you can perform an extra postprocessing step, applying modifications on the extracted tokens.
  This is where you can perform spell correction, word normalization and segmentation and decide which tokens to omit, normalize or annotate (surround or replace with special tags).

### Spell Correction
The Spell Corrector extends the functionality of Peter Norvig's spell-corrector.

### Word Segmentation
Word Segmentation that implements the Viterbi algorithm for word segmentation. Based on CH14 from the book Beautiful Data (Segaran and Hammerbacher, 2009)





#### References

[1]K. Gimpel et al., “Part-of-speech tagging for twitter: Annotation, features, and experiments,” in Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies: short papers-Volume 2, 2011, pp. 42–47.

[2]C. Potts, “Sentiment Symposium Tutorial: Tokenizing,” Sentiment Symposium Tutorial, 2011. [Online]. Available: http://sentiment.christopherpotts.net/tokenizing.html.
