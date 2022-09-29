from functools import reduce
import operator
import os
from os import path
from os.path import expanduser
import sys
import ujson as json
from urllib.request import urlretrieve
import zipfile
from ekphrasis.dicts import emojidict
from ekphrasis.dicts.noslang import slangdict
import pickle

def get_stats_dir():
    home = expanduser("~")

    ekphrasis_dir = path.join(home, '.ekphrasis')

    if not os.path.exists(ekphrasis_dir):
        os.makedirs(ekphrasis_dir)

    stats_dir = path.join(ekphrasis_dir, 'stats')

    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)

    return stats_dir


def parse_stats(name, sep='\t', ngram_sep='_'):
    """
    Read key,value pairs from file.
    """
    print("reading ngrams", name)
    d = {}
    with open(name, "r", encoding="utf-8") as f:
        for line in f:
            values = line.split(sep)
            if len(values) > 2:
                d[ngram_sep.join(values[:-1])] = int(values[-1])
            else:
                d[values[0]] = int(values[1])

    return d


def read_stats(corpus, ngram):
    stats_dir = get_stats_dir()
    check_stats_files()
    print("Reading " + "{} - {}grams ...".format(corpus, ngram))
    text = path.join(*[stats_dir, corpus, "counts_{}grams.txt".format(ngram)])
    dumped = path.join(
        *[stats_dir, corpus, "counts_{}grams.json".format(ngram)])

    if os.path.isfile(dumped):
        with open(dumped, "r") as f:
            stats = json.load(f)
            return stats
    elif os.path.isfile(text):
        print("generating cache file for faster loading...")
        stats = parse_stats(text)
        with open(dumped, "w") as f:
            json.dump(stats, f)
        return stats
    else:
        print("stats file not available!")
        sys.exit(1)


def read_emoji():
    home = expanduser("~")

    ekphrasis_dir = path.join(home, '.ekphrasis')

    if not os.path.exists(ekphrasis_dir):
        os.makedirs(ekphrasis_dir)
    if not os.path.isfile(os.path.join(ekphrasis_dir,'uni_emoticon.pickle')):
        print('Emoji File not found..\nDownloading')
        z = emojidict.get_emoji()
        print('done!')        
        pickle.dump(z, open(os.path.join(ekphrasis_dir,'uni_emoticon.pickle'), "wb"))
        return z
    else:
        print('Reading Emoticons ...')
        z = pickle.load(open(os.path.join(ekphrasis_dir,'uni_emoticon.pickle'), 'rb'))
        return z
    

def gen_slang_dict():
    home = expanduser("~")

    ekphrasis_dir = path.join(home, '.ekphrasis')

    if not os.path.exists(ekphrasis_dir):
        os.makedirs(ekphrasis_dir)
    if not os.path.isfile(os.path.join(ekphrasis_dir,'slangdict.pickle')):
        print('Slang File not found..\nGenerating')
        z = slangdict.get_slang()
        print('done!')        
        pickle.dump(z, open(os.path.join(ekphrasis_dir,'slangdict.pickle'), "wb"))
        return z
    else:
        print('Reading Slangs ...')
        z = pickle.load(open(os.path.join(ekphrasis_dir,'slangdict.pickle'), 'rb'))
        return z

def listdir_nohidden(path):
    return [f for f in os.listdir(path) if not f.startswith('.')]


def download_statistics():
    stats_dir = get_stats_dir()
    print("Word statistics files not found!\nDownloading...", end=" ")
    # url = "https://www.dropbox.com/s/a84otqrg6u1c5je/stats.zip?dl=1"
    url = "https://data.statmt.org/cbaziotis/projects/ekphrasis/stats.zip"
    urlretrieve(url, "stats.zip")
    print("done!")

    print("Unpacking...", end=" ")
    with zipfile.ZipFile("stats.zip", "r") as zip_ref:
        zip_ref.extractall(stats_dir)

    os.remove("stats.zip")
    print("done!")


def check_stats_files():
    stats_dir = get_stats_dir()
    if not os.path.exists(stats_dir) or len(listdir_nohidden(stats_dir)) == 0:
        download_statistics()


def product(nums):
    """
    Return the product of a sequence of numbers.
    """
    return reduce(operator.mul, nums, 1)

def remove_tags(doc):
    """
    Remove tags from sentence
    """
    doc = ' '.join(word for word in doc.split() if word[0]!='<')
    return doc

# check_stats_files()
