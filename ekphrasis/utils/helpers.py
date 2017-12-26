import operator
import os
import sys
import ujson as json
import zipfile
from functools import reduce
from os import path
from urllib.request import urlretrieve

stats_dir = path.join(os.path.dirname(os.path.dirname(__file__)), 'stats')


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


def listdir_nohidden(path):
    return [f for f in os.listdir(path) if not f.startswith('.')]


def check_stats_files():
    if not os.path.exists(stats_dir) or len(listdir_nohidden(stats_dir)) == 0:
        print("Word statistics files not found!\nDownloading...", end=" ")
        url = "https://www.dropbox.com/s/a84otqrg6u1c5je/stats.zip?dl=1"
        urlretrieve(url, "stats.zip")
        print("done!")

        print("Unpacking...", end=" ")
        with zipfile.ZipFile("stats.zip", "r") as zip_ref:
            zip_ref.extractall(stats_dir)

        os.remove("stats.zip")
        print("done!")


def product(nums):
    """
    Return the product of a sequence of numbers.
    """
    return reduce(operator.mul, nums, 1)
