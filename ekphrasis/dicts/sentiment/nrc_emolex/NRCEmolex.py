import csv
import os
import pickle

'''
NRC Word-Emotion Association Lexicon (aka EmoLex) (14.000 entries)
--------------------------------------
format = dictionary with entries like this:
word1={'negative': 0.0, 'positive': 1.0, 'surprise': 0.0, 'trust': 0.0, 'joy': 1.0, 'fear': 0.0, 'anticipation': 0.0, 'sadness': 0.0, 'anger': 0.0, 'disgust': 0.0}
'''


class NRCEmolex:
    def __init__(self):
        super().__init__()
        self.raw_filename = "NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
        self.parsed_filename = "emolex.pickle"

    def write(self):
        if os.path.exists(
                os.path.join(os.path.dirname(__file__), self.raw_filename)):
            with open(
                    os.path.join(os.path.dirname(__file__), self.raw_filename),
                    "r") as f:
                reader = csv.reader(f, delimiter="\t")
                reader = list(reader)
                lexicon = {}
                for row in reader:
                    # lexicon[row[0]][row[1]] = float(row[2])
                    lexicon.setdefault(row[0], {})[row[1]] = float(row[2])

                for k, v in lexicon.items():
                    polarity = 0
                    if lexicon[k]["positive"]:
                        polarity = 1
                    elif lexicon[k]["negative"]:
                        polarity = -1
                    lexicon[k]["polarity"] = polarity

                    lexicon[k]["emotions"] = [v['fear'], v['sadness'],
                                              v['trust'], v['disgust'],
                                              v['surprise'],
                                              v['anger'], v['joy'],
                                              v['anticipation']]

                with open(self.parsed_filename, 'wb') as pickle_file:
                    pickle.dump(lexicon, pickle_file)
        else:
            print("input file not found!")

    def read(self):
        if os.path.exists(
                os.path.join(os.path.dirname(__file__), self.parsed_filename)):
            with open(os.path.join(os.path.dirname(__file__),
                                   self.parsed_filename), 'rb') as f:
                data = pickle.load(f)
                return data
        else:
            self.write()
            return self.read()

# NRCEmolex().write()
# NRCEmolex().read()
