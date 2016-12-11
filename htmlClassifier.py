#!/usr/bin/env python3

import nltk
from nltk.corpus import CategorizedPlaintextCorpusReader as Reader
import random
import re
import pickle
import htmlParser
import htmlToTxtMaker
import textblob.classifiers
import sys

"""
htmlClassifier.py
Created by Brandon Dutko
To be used with htmlToTxtMaker, htmlParser, nltk, and textblob.
A NaiveBayes classifier designed to determine if a website is
"Good" or "Bad" determined by parsed data stored in ./data/trainingGood/
and ./data/trainingBad made with htmlToTxtMaker.py and htmlParser.py.

Use: ./htmlClassifier.py (RETRAIN) (TEST)
Flags:
    RETRAIN:
        If set the classifier will be retrained using the parsed data in
        data/<categories>/ folders.
    TEST:
        If set the classifier will use some of the data in data/<categories>/
        folders as a test set and output the classifier's accuracy.
        Recommended to only use with retrain for most accurate results.
        Not recommended to use with retrain for best trained classifier
        unless you run the program again with only retrain flag set.
    RETRAIN+TEST:
        If both flags are set then the classifier will not be trained with
        all of the data but rather a random selection of 75% of it and tested
        with the other 25%.
"""

RETRAIN_CLASSIFIER = False
TESTING = False

#Get flags from command line
if(__name__ == "__main__"):
    argLen = len(sys.argv)
    if(argLen > 1):
        if("RETRAIN" in argv):
            RETRAIN_CLASSIFIER = True
        if("TEST" in argv):
            TESTING = True

classifier = None

def retrain():
    """
    Trains a textblob NaiveBayesClassifier and dumps it to a pickle in
    ./Dill/classifier.pickle
    """

    print("Generating Training Corpus...")
    trainingCorpus = Reader("./data/", r'training.*\.txt', cat_pattern=r'training(\w+).*\.txt')
    print("Training Corpus generated")
    textSet = []
    print("Generating text set...")
    for f in trainingCorpus.fileids(categories = "Good"):
        text = trainingCorpus.words(f)
        textSet.append((text, "Good"))
    for f in trainingCorpus.fileids(categories = "Bad"):
        text = trainingCorpus.words(f)
        textSet.append((text, "Bad"))
    print("Shuffling...")
    random.shuffle(textSet)
    print("Training...")
    if(TESTING):
        classifier = textblob.classifiers.NaiveBayesClassifier(textSet[:(len(textSet)//2)+(len(textSet)//4)])
        print("Trained")
    else:
        classifier = textblob.classifiers.NaiveBayesClassifier(textSet)
        print("Dumping to pickle...")
        with open('Dill/classifier.pickle', 'wb') as f:
            pickle.dump(classifier, f)

if(RETRAIN_CLASSIFIER):
    retrain()
else:
    try:
        print("Retrieving trained classifier from pickle...")
        with open('Dill/classifier.pickle', 'rb') as f:
            classifier = pickle.load(f)
    except:
        print("Error retrieving classifier from pickle")
        print("Are you sure there is a pickled trained classifier in Dill/classifier.pickle?")
        print("Try setting retrain_classifier to True if you want to make one.")
        exit()

if(TESTING):
    print("Testing...")
    print("Accuracy:", classifier.accuracy(textSet[(len(textSet)//2)-(len(textSet)//4):]))
elif(__name__ == "__main__"):
    """
    Loop asking for a URL, parse the html from the url and classify that
    with the classifier.
    """

    print("Type 'quit' to exit.")
    doLoop = True
    first = True
    while(doLoop):
        if(first):
            print("Note: The first time always takes awhile.")
            first = False
        url = input("URL: ")
        if(url[:4] == "quit"):
            break
        if(url[:4] != "http"):
            url = "http://"+url
        try:
            print("Fetching url...")
            html = htmlToTxtMaker.getPage(url)
        except:
            print("That url seems to be unreachable at this time.")
            continue
        print("Parsing...")
        html = htmlParser.htmlParser(html)
        print("Classifying...")
        print(classifier.classify(html))
    exit()

def testURL(url):
    """
    Returns wether the URL is good or bad.
    """
    if(url[:4] != "http"):
        url = "http://"+url
    try:
        html = htmlToTxtMaker.getPage(url)
    except:
        raise IndexError
    html = htmlParser.htmlParser(html)
    return classifier.classify(html)

def testHTML(html):
    """
    Takes raw html, parses it then returns the good or bad classification.
    Use this to not duplicate requests if you already are requesting from
    a url.
    """
    html = htmlParser.htmlParser(html)
    return classifier.classify(html)
