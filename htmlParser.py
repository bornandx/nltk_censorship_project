from bs4 import BeautifulSoup
from nltk import Text
from nltk import word_tokenize


def htmlParser(html):
    htmlText = BeautifulSoup(html,"html.parser").get_text()
    text = nltk.Text(word_tokenize(htmlText))
    return text


    
