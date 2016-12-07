from bs4 import BeautifulSoup



def htmlParser(html):
    htmlText = BeautifulSoup(html,'html.parser')
    cleanHtmlText = htmlText.prettify()
    htmlText = cleanHtmlText.get_text()
    return htmlText


    
