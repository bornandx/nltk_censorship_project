#!/usr/bin/env python3

import nltk
import urllib.request
import re

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
        html = urllib.request.urlopen(request).read()
    except:
        raise IndexError
    return str(html)

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
                lineNoSlash = re.sub(r'http://','',line)
                lineNoSlash = re.sub(r'https://','',line)
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

def censMain(BadTrainingFile, GoodTrainingFile):
    """
    Top level logic for running the program.
    """
    getTrainingData(GoodTrainingFile)
    getTrainingData(BadTrainingFile)
    
    dataset = sklearn.datasets.load_files("data/")
    for something in dataset:
        print(something, type(dataset[something]))
    for name in dataset["target_names"]:
        print("NAME:",name)

censMain("trainingBad.txt", "trainingGood.txt")
