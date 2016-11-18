#!/usr/bin/env python3

import nltk

import os
os.chdir(os.getcwd())

from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier

def getPage(string):
    """
    Takes a weburl as a string and gets the html off the internet.  If the
    page can't be retrieved for some reason then raise an IndexError.
    (because internet[thatpage] doesn't exist or couldn't be reached <.< )
    """
    html = ""
    #TODO
    return html

def getTrainingData(afile):
    """
    Takes a file path/name and creates the training blocks of text from the
    weburls listed in the file.  Returns a list of html pages as strings.

    (Should we parse the html code or not?  It could be relevant to determining
    if the page should be censored?)
    """
    data = []
    with open(afile, 'r') as trainFile:
        for line in trainFile:
            line = line.rstrip() #strip newlines
            if not line:
                continue
            data.append(getPage(line))
    return data

def censMain(BadTrainingFile, GoodTrainingFile):
    """
    Top level logic for running the program.
    """
    goodData = getTrainingData(GoodTrainingFile)
    badData = getTrainingData(BadTrainingFile)
    #TODO
