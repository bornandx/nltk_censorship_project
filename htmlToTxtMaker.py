#!/usr/bin/env python3

import urllib.request

PRINTPROCESSINGURLS = True
PRINTERRORS = True

def getPage(string):
    """
    Takes a weburl as a string and gets the html off the internet.
    If the page can't be retrieved for some reason then raise an IndexError.
    """

    #Lots of sites block non browser user agents so let's fake being a browser.
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent,}

    try:
        request = urllib.request.Request(string, None, headers)
        html = urllib.request.urlopen(request, timeout=5).read()
    except:
        if(PRINTERRORS):
            print("FAILED REQUEST FOR "+string)
        raise IndexError
    return str(html)

def setTempData(string):
    """
    Takes a string rep of a url and stores the html from that url in a .txt
    file.
    """
    with open("tempData/temp/current.txt", 'w') as tempFile:
        try:
            tempHTML = getPage(string)
            for line in tempHTML:
                tempFile.write(line)
        except:
            if(PRINTERRORS):
                print("Error processing "+string)
            raise IndexError

def setTrainingData(filePath):
    """
    Takes a file path for a file that lists webUrls, gets the html from those
    urls and stores those in files to be used as training data.
    """

    with open(filePath, 'r') as trainFile:
        i = 0
        for line in trainFile:
            i += 1
            line = line.rstrip() #strip newlines
            if(PRINTPROCESSINGURLS):
                print("GETTING:: "+line)
            if not line:
                continue
            try:
                if(line[:4] != "http"):
                    line = "http://"+line
                html = getPage(line)
                with open("data/"+filePath.rsplit("/", 1)[-1].rsplit(".", 1)[0]+"/" + str(i) + ".txt", 'w') as htmlFile:
                    for htmlLine in html:
                        htmlFile.write(htmlLine)
                if(PRINTERRORS):
                    print("MADE/UPDATED:: "+htmlFile.name)
            except:
                if(PRINTERRORS):
                    print("Error for "+line)
                continue

def test():
    PRINTPROCESSINGURLS = True
    PRINTERRORS = True
    filePaths = ["training/trainingGood.txt", "training/trainingBad.txt"]
    for path in filePaths:
        setTrainingData(path)

if __name__ == "__main__":
    test()
