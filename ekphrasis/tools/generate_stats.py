import argparse
import glob
import html
import os
import pickle
import re
import time
from collections import Counter
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy
from tqdm import tqdm

REGEX_TOKEN = re.compile(r'(?<![#@])\b[a-z]{1,15}\b')
REGEX_URL = re.compile(
    r"(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})")
SEPARATOR = "_"


###############################################################################
# Parse Arguments
###############################################################################

def check_empty_arg(value):
    if len(str(value)) == 0:
        raise argparse.ArgumentTypeError("Invalid argument - no value passed.")
    return value


def parse_int_list(value):
    if len(str(value)) == 0:
        raise argparse.ArgumentTypeError("Invalid argument - no value passed.")

    return [int(x) for x in value.split(",")]


parser = argparse.ArgumentParser()

# add arguments ########################################
parser.add_argument('--input', nargs='?', type=check_empty_arg, default="./",
                    help='path to file or directory containing the files for '
                         'calculating the statistics.')
parser.add_argument('--name', nargs='?', type=check_empty_arg,
                    default="mycorpus", help='')
parser.add_argument('--ngrams', type=int, default=2,
                    help='up-to how many ngrams to calculate statistics.')
parser.add_argument('--mincount', nargs='+', type=int, default=[60, 25],
                    help='eliminate all ngrams below the given count.')
parser.add_argument('--perc', nargs='+', type=int, default=0,
                    help='eliminate all ngrams below the given percentile. '
                         '0=ALL')

pickle_parser = parser.add_mutually_exclusive_group()
pickle_parser.add_argument('--pickle', dest='pickle', action='store_true')
pickle_parser.add_argument('--no-pickle', dest='pickle', action='store_false')
parser.set_defaults(pickle=False)

web_parser = parser.add_mutually_exclusive_group()
web_parser.add_argument('--web-fix', dest='web_fix', action='store_true')
web_parser.add_argument('--no-web-fix', dest='web_fix', action='store_false')
parser.set_defaults(web_fix=True)

args = parser.parse_args()


###############################################################################

def tokenize(text):
    """
    extract words from text
    :param text:
    :return:
    """
    if args.web_fix:
        text = REGEX_URL.sub(' ', text)
        text = html.unescape(text)
    return REGEX_TOKEN.findall(text.lower())


def get_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


def write_stats_to_file(file, counts, mincount):
    with open(file, 'w', encoding="utf-8") as f:
        if args.perc == 0:
            percentile = 0
        else:
            percentile = numpy.percentile(
                numpy.fromiter(counts.values(), numpy.int32), args.perc)
        threshold = max(percentile, mincount)

        for k, v in counts.items():

            if v >= threshold:
                entry = k.split(SEPARATOR)
                entry.append(str(v))
                f.write('\t'.join(entry) + '\n')

    if args.pickle:
        with open(file + ".pickle", 'wb') as f:
            pickle.dump(counts, f)


def count_file(filename, countkeeper, desc=""):
    """
    Count the word statistics of a file
    :param desc:
    :param filename:
    :param countkeeper:
    :return:
    """
    print()
    print("computing statistics for file: ", filename)
    with open(filename, "r", encoding="utf-8", errors='ignore') as infile:
        num_lines = sum(1 for line in open(filename, "r", encoding="utf-8"))
        for line in tqdm(infile, total=num_lines, desc=desc):
            try:
                toks = tokenize(line)
                for i in range(args.ngrams):
                    ngram = i + 1
                    if ngram > 1:
                        toks = ["<S>"] + toks
                    for token in get_ngrams(toks, ngram):
                        countkeeper[ngram][SEPARATOR.join(token)] += 1
            except Exception as e:
                print("ERROR - ", e, infile)


def write_stats(counts):
    print()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for k, v in counts.items():
        print("Writing " + str(k) + "-grams...")
        counter = Counter(counts[k])
        print("entries:{}\t-\ttokens:{}".format(format(len(counter), ','),
                                                format(sum(counter.values()),
                                                       ',')))

        name = "counts_{}grams.txt".format(str(k))
        filename = os.path.join(dir_path, "..", "stats", args.name, name)

        print("writing stats to file {}".format(filename))
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        write_stats_to_file(filename, counter, args.mincount[int(k) - 1])


def prune_low_freq(word_stats, threshold):
    """
    remove ngrams with count less than mincount
    avoid dict comprehension as it creates a new temp dict
    and overloads the memory
    Args:
        word_stats ():
        threshold ():

    Returns:

    """
    for ng in list(word_stats.keys()):
        for t in list(word_stats[ng].keys()):
            if not word_stats[ng][t] >= threshold:
                del word_stats[ng][t]


def plot_statistics(statistics):
    fig = plt.figure(figsize=(5 * len(statistics), 5))
    for i, (k, v) in enumerate(statistics.items()):
        ax = fig.add_subplot(1, len(statistics), i + 1)
        ax.set_title("{}-gram - total={}".format(k, len(v)))
        ax.grid(True)
        values = numpy.fromiter(statistics[k].values(), numpy.int32)
        ax.hist(values, bins=100, range=(0, 100))
    fig.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()


if __name__ == '__main__':
    plt.ion()  # set plot to animated
    stats = defaultdict(lambda: defaultdict(int))
    pruning_size_threshold = 5000000
    low_freq_threshold = 3

    if os.path.isfile(args.input):
        count_file(args.input, stats)
        time.sleep(0.01)
        prune_low_freq(stats, 1)
        write_stats(stats)

    elif os.path.isdir(args.input):
        files = glob.glob(args.input + "*.txt")
        for i, file in enumerate(files):
            try:
                count_file(file, stats, str(i + 1) + "/" + str(len(files)))
            except Exception as e:
                print("ERROR - ", e, file)

            time.sleep(0.01)

            if any(len(stats[ngram]) > pruning_size_threshold for ngram in
                   list(stats.keys())):
                print("Cleaning entries with only one occurrence, "
                      "in order to save memory...")
                prune_low_freq(stats, low_freq_threshold)
                # write progress
                # plot_statistics(stats)

            write_stats(stats)

        prune_low_freq(stats, low_freq_threshold)
        write_stats(stats)
    else:
        print("Wrong input. Give a file or directory!")
