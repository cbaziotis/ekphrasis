from functools import reduce
import operator
import os
from os import path
from os.path import expanduser
import sys
import ujson as json
from urllib.request import urlretrieve
import zipfile


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


def listdir_nohidden(path):
    return [f for f in os.listdir(path) if not f.startswith('.')]


def download_statistics():
    stats_dir = get_stats_dir()
    print("Word statistics files not found!\nDownloading...", end=" ")
    url = "https://www.dropbox.com/s/a84otqrg6u1c5je/stats.zip?dl=1"
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

# check_stats_files()
