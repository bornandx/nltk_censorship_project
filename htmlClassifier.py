#!/usr/bin/env python3

import nltk
from nltk.corpus import CategorizedPlaintextCorpusReader as Reader

trainingCorpus = Reader("./data/", r'training.*\.txt', cat_pattern=r'training(\w+).*\.txt')
print(trainingCorpus.words(categories="Bad")[:50])
print(trainingCorpus.fileids(categories="Bad"))
print(trainingCorpus.categories())
