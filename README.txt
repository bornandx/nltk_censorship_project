----------------README----------------------------------------

You will need 2 libraries to run this project 

NLTK: http://www.nltk.org/
TextBlob: https://textblob.readthedocs.io/en/dev/

The scripts should be ran in this order:

    1.) run htmlClassifier.py to use the trained pickled classifier if the
    classifier has already been trained.

    OR
    [DO THIS FOR FIRST TIME USE]
    1.) run htmlClassifier.py RETRAIN to remake/retrain the classifier with the
    data in data/trainingGood and data/trainingBad plus do the user URL input.
    NOTE: This only works if there is already parsed data in data/trainingBad
    and data/trainingGood.  (Which there should be)

    OR (If you want to update the data/changed trainingBad.txt and/or
    trainingGood.txt to represent different good/bad sites)

    0.) Delete anything in data/trainingGood and data/trainingBad.

    1.) run htmlToTxtMaker.py to fetch the data from the net.
    2.) run htmlParser.py to parse the data.

    Once the data is fetched and parsed it is stored under data/ and doesn't
    need to be fetched/parsed again unless you want to update the data.
    NOTE: If you want to update the data make sure to delete any old data
    found in data/trainingBad and data/trainingGood first.

    3.) run htmlClassifier.py RETRAIN to remake/retrain the classifier with the
        newly fetched/parsed data plus do the user URL input.

    NOTE: htmlClassifier RETRAIN TEST is not ideal to use 
    as the final trained classifier as it won't be trained on all of the data.
    htmlClassifier TEST will ignore the TEST flag as the script is set
    to only test newly trained classifiers simply for use when testing the
    use of datasets/features/parsers.

    This project is saved in publicly available github repository.
    REPO: https://github.com/bornandx/nltk_censorship_project.git
