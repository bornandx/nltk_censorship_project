#!/usr/bin/env python3

import os, numpy

NEWLINE = '\n'
SKIP_FILES = {'cmds'}


def read_files(path):
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            if file_name not in SKIP_FILES:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    past_header, lines = True, []
                    f = open(file_path, "r")
                    for line in f:
                        if past_header:
                            lines.append(line)
                        elif line == NEWLINE:
                            past_header = True
                    f.close()
                    content = NEWLINE.join(lines)
                    yield file_path, content

from pandas import DataFrame


def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text': text, 'class': classification})
        index.append(file_name)

    data_frame = DataFrame(rows, index=index)
    return data_frame

GOOD = 'good'
BAD = 'bad'

SOURCES = [
    ('data/trainingGood', GOOD),
    ('data/trainingBad', BAD),
]

data = DataFrame({'text': [], 'class': []})
for path, classification in SOURCES:
    data = data.append(build_data_frame(path, classification))

data = data.reindex(numpy.random.permutation(data.index))

import numpy
from sklearn.feature_extraction.text import CountVectorizer

count_vectorizer = CountVectorizer()
counts = count_vectorizer.fit_transform(data['text'].values)

from sklearn.naive_bayes import MultinomialNB

classifier = MultinomialNB()
targets = data['class'].values
classifier.fit(counts, targets)

examples = [""]
example_counts = count_vectorizer.transform(examples)
predictions = classifier.predict(example_counts)
print(predictions) # [1, 0]
