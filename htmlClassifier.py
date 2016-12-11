#!/usr/bin/env python3

import nltk
from nltk.corpus import CategorizedPlaintextCorpusReader as Reader
import random
import statistics
import re
import pickle

RETRAIN_CLASSIFIER = False
TESTING = False
"""
Set TESTING to test 
Set UPDATE_CORPUS if the corpus has been updated.  You can also force update
the corpus by deleting the Dill/corpus.pickle file.
Set RETRAIN_CLASSIFIER if the classifier should be re-trained.  Re-training
is forced if the Dill/classifier.pickle file is deleted or if the corpus is
updated.
"""

SMALL, MEDIUMSM, MEDIUM, MEDIUMLG, LARGE = 0,0,0,0,0

if(RETRAIN_CLASSIFIER):
    print("Generating Training Corpus...")
    trainingCorpus = Reader("./data/", r'training.*\.txt', cat_pattern=r'training(\w+).*\.txt')
    print("Training Corpus generated")

def Category_features(word, text, wordIndex):
    """
    Returns the word, the word + the previous word, and the word + the next
    word.
    """
    before=word
    after=word
    surrounded=word
    try:
        before+=text[wordIndex-1]
        surrounded = text[wordIndex-1]+surrounded
    except:
        """Do nothing"""
    try:
        after+=text[wordIndex+1]
        surrounded+=text[wordIndex+1]
    except:
        """Do nothing"""
    return {'word':word, 'previous':before, 'next':after, 'surrounding':surrounded}

def Category_whole_text_features(tokenized_text):
    """
    Return the size of the text generalized as small, medium-small, medium, medium-large, or large based on predetermined sizes obtained with the maximum text size, minimum text size and average text size.
    Add more features for more accuracy.
    """
    length = len(tokenized_text)
    size = 'undefined'
    if(length <= ((MEDIUMSM + SMALL)/2)):
        size = "small"
    elif(length <= ((MEDIUMSM + MEDIUM)/2)):
        size = "medium-small"
    elif(length <= ((MEDIUM + MEDIUMLG)/2)):
        size = "medium"
    elif(length <= ((MEDIUMLG + LARGE)/2)):
        size = "medium-large"
    else:
        size = "large"

    isPron = False
    hasXXX = False
    hasTrump = False
    isVulgar = False
    hasGit = False
    hasMeme = False
    hasDownload = False
    for word in tokenized_text:
        if(re.search(r'[dD][oO][wW][nN][lL][oO][aA][dD]', word) != None):
            hasDownload = True
        if(re.search(r'([pP][oO][rR][nN])|([sS][eE][xX])',word) != None):
            isPron = True
        if(re.search(r'[xX][xX][xX]', word) != None):
            hasXXX = True
        if(re.search(r'[tT][rR][uU][mM][pP]', word) != None):
            hasTrump = True
        if(re.search(r'[gG][iI][tT]', word) != None):
            hasGit = True
        if(re.search(r'([mM][eE][mM][eE])|([lL][oOeE][lL])|([kK][eE][kK])|([wW][tT][fF])|([kK][yY][sS])|([dD][oO][gG][eE])|([dD][oO][lL][aA][nN])|([pP][eE][pP][eE])|([wW][aA][iI][fF][uU])|([dD][aA][nN][kK])|([yY][oO][lL][oO])|([cC][aA][nN][cC][eE][rR])', word) != None):
            hasMeme = True
        if(re.search(r'([fF][uU][cC][kK])|([aA][sS][sS])|([dD][iI1!][cC][kK])|([bB8][iI1!][tT][cC][hH])|([cC][uU][nN][tT])|([pP][uU][sS][sS][yY])|([nN][iI1!][gG][gG])|([cC][oO0][cC][kK])|([sS][hH][iI1!][tT])|([bB8][aA][sS][tT][aA][rR][dD])|([wW][hH][oO0][rR][eE3])|([fF][aA][gG])', word) != None):
            isVulgar = True
    return {'size':size, 'pron':isPron, 'xxxPresent':hasXXX, 'Trump':hasTrump, 'Vulgar':isVulgar, 'Git':hasGit, 'Meme':hasMeme, 'dl':hasDownload}

def Set_sizes(corpus):
    sizes = []
    for f in corpus.fileids():
        sizes.append(len(corpus.words(f)))
    MEDIUM = statistics.median(sizes)
    LARGE = max(sizes)
    SMALL = min(sizes)
    MEDIUMSM = statistics.mean([MEDIUM, SMALL])
    MEDIUMLG = statistics.mean([MEDIUM, LARGE])

whole_labeled_text = []
def Gen_labeled_texts():
    print("Generating labeled texts...")
    for f in trainingCorpus.fileids(categories='Good'):
        whole_labeled_text.append((trainingCorpus.words(f), 'Good'))
    for f in trainingCorpus.fileids(categories='Bad'):
        whole_labeled_text.append((trainingCorpus.words(f), 'Bad'))
    random.shuffle(whole_labeled_text)
    print("labeled texts generated")

featuresets = []
def Gen_feature_sets():
    print("generating featuresets...")
    for (t, category) in whole_labeled_text:
        wholeFeatures = Category_whole_text_features(t)
        i = -1
        for n in t:
            i += 1
            features = Category_features(n, t, i)
            features.update(wholeFeatures)
            featuresets.append((features, category))
    random.shuffle(featuresets)
    print("featuresets generated")

if(RETRAIN_CLASSIFIER):
    Gen_labeled_texts()
    Gen_feature_sets()

print("Size " + str(len(featuresets)))
if(TESTING):
    #Note that the train_set is irrelevant if the classifier is retrieved
    #From the pickle
    train_set = featuresets[len(featuresets)//2:]
    test_set = featuresets[:len(featuresets)//2]
elif(RETRAIN_CLASSIFIER):
    train_set = featuresets
    test_set = []

if(not RETRAIN_CLASSIFIER):
    try:
        print("Retrieving trained classifier from pickle...")
        with open('Dill/classifier.pickle', 'rb') as f:
            classifier = pickle.load(f)
        print("Successfully retrieved classifier from pickle")
    except:
        print("Failed retrieval of classifier from pickle")
        print("Are you sure there is a classifier stored at Dill/classifier.pickle?")
        quit()
else:
    print("Training...")
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("Trained")
    print("Dumping classifier to pickle...")
    with open('Dill/classifier.pickle', 'wb') as f:
        pickle.dump(classifier, f)
    print("Successfully dumped to pickle")

if(TESTING):
    print("Testing...")
    print("Accuracy "+str(nltk.classify.accuracy(classifier, test_set)))
    print(classifier.show_most_informative_features(20))
else:
    while(True):
        testUrl = input("Enter URL: ")
        #TODO get the html, parse it, get classification from classifier
"""
print(labeled_text[:50])
print(trainingCorpus.words(categories="Bad")[:50])
print(trainingCorpus.fileids(categories="Bad"))
print(trainingCorpus.categories())
"""
