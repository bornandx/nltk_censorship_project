#!/usr/bin/env python3

from bs4 import BeautifulSoup
from nltk import word_tokenize
import nltk
import os


def htmlParser(html):
    htmlText = BeautifulSoup(html,"html.parser").get_text()
    text = nltk.Text(word_tokenize(htmlText))
    return text

if __name__ == "__main__":
    """
    Tokenize the training data.
    """
    for root, dirs, files in os.walk("./data"):
        for f in files:
            print("Parsing "+root+"/"+f)
            filestring = ""
            with open(os.path.join(root, f), 'r') as htmlFile:
                for line in htmlFile:
                    filestring = filestring + line
            tokenizedText = htmlParser(filestring)
            with open(os.path.join(root, f), 'w') as htmlFile:
                for word in tokenizedText:
                    htmlFile.write(word+" ")
