#!/usr/bin/env python3

import nltk
import urllib.request
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from pandas import DataFrame

import os
os.chdir(os.getcwd())

from sklearn.svm import LinearSVC
import sklearn
from nltk.classify.scikitlearn import SklearnClassifier

#TODO make this a command line arg
MAKETRAINING = False

def getPage(string):
    """
    Takes a weburl as a string and gets the html off the internet.  If the
    page can't be retrieved for some reason then raise an IndexError.
    (because internet[thatpage] doesn't exist or couldn't be reached <.< )
    """

    #Lots of sites block non browser user agents so let's fake being a browser.
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent,}

    try:
        request = urllib.request.Request(string, None, headers)
        html = urllib.request.urlopen(request, timeout=5).read()
    except:
        raise IndexError
    return str(html)

def getData(string):
    """
    Takes a string rep of a url and stores the html in a .txt file that is
    used to make the dataset using sklearn.datasets.load_files.
    """
    with open("tempData/temp/current.txt", 'w') as tempFile:
        tempFile.write(getPage(string))
    return sklearn.datasets.load_files("tempData")

def getTrainingData(afile):
    """
    Takes a file path/name and creates the training blocks of text from the
    weburls listed in the file.  Stores the html in .txt files in proper
    subfolders to later be turned into datasets with
    sklearn.datasets.load_files.

    (Should we parse the html code or not?  It could be relevant to determining
    if the page should be censored?)
    """

    #Make the .txt to be turned into datasets
    if(MAKETRAINING):
        with open("training/"+afile, 'r') as trainFile:
            for line in trainFile:
                line = line.rstrip() #strip newlines
                lineNoSlash = re.sub(r'https','',line)
                lineNoSlash = re.sub(r'http','',lineNoSlash)
                lineNoSlash = re.sub(r'www.','',lineNoSlash)
                lineNoSlash = re.sub(r'[/<>:"\|?*]','', lineNoSlash)
                print(lineNoSlash)
                if not line:
                    continue
                try:
                    with open("data/"+afile[:-4]+"/"+lineNoSlash+".txt", 'w') as htmlFile:
                        htmlFile.write(getPage(line))
                except:
                    print("Error for "+line)
                    continue

def read_files(path):
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                past_header, lines = False, []
                f = open(file_path)
                for line in f:
                    if past_header:
                        lines.append(line)
                    elif line == NEWLINE:
                        past_header = True
                    f.close()
                    content = NEWLINE.join(lines)
                    yield file_path, content

def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text':text, 'class':classification}
        index.append(file_name)

    data_frame = DataFrame(rows, index=index)
    return data_frame

SOURCES = [
    ('data/trainingGood', 'good'),
    ('data/trainingBad', 'bad')
]

data = DataFrame({'text': [], 'class':[]})
for path, classification in SOURCES:
    data = data.append(build_data_frame(path, classification))

data = data.reindex(numpy.random.permutation(data.index))

from sklearn.feature_extraction.text import CountVectorizer
count_vectorizer = CountVectorizer()
counts = count_vectorizer.fit_transform(data['text'].values)

classifier = MultinomialNB()
targets = data['class'].values
classifier.fit(counts, targets)

def censMain(BadTrainingFile, GoodTrainingFile):
    """
    Top level logic for running the program.
    """
    getTrainingData(GoodTrainingFile)
    getTrainingData(BadTrainingFile)
    
    trainingset = sklearn.datasets.load_files("data/")
    #TODO Build data_frame
    data = DataFrame({'text': [], 'class': []})
    print(trainingset.filenames)
    

censMain("trainingBad.txt", "trainingGood.txt")
