import os

import pickle


def read_slangdict():
    filename = os.path.join(os.path.dirname(__file__), "slangdict.pickle")
    if os.path.isfile(filename):
        print("Reading data...")
        data = pickle.load(open(filename, 'rb'))
        return data
