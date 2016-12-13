----------------README----------------------------------------

You will need 2 libraries to run this project 

NLTK: http://www.nltk.org/
TextBlob: https://textblob.readthedocs.io/en/dev/

The scripts should be ran in this order:

    1.) htmlClassifier.py to use the pre-trained pickled classifier
    provided (not in git)(which is overwritten when the classifier is
    retrained).  Do this if you don't want to wait to retrain the
    classifier or fetch html from hundreds of sites (many of which are
    very unreputable) which will take a while (It takes my laptop about
    40 minutes for the entire process).

    OR

    1.) htmlToTxtMaker.py to fetch the data from the net.
    2.) htmlParser.py to parse the data.

    Once the data is fetched and parsed it is stored under data/ and doesn't
    need to be fetched/parsed again unless you want to update the data.
    NOTE: If you want to update the data make sure to delete any old data
    found in data/trainingBad and data/trainingGood first.

    3a.) htmlClassifier.py RETRAIN to remake/retrain the classifier with the
        newly fetched/parsed data plus do the user URL input.
    3b.) htmlClassifier.py RETRAIN TEST to remake/retrain and test the pickle
        plus do the user URL input.

    NOTE: htmlClassifier RETRAIN TEST is not ideal to use 
    as the final trained classifier as it won't be trained on all of the data.
    htmlClassifier TEST will ignore the TEST flag as the script is set
    to only test newly trained classifiers simply for use when testing the
    use of datasets/features/parsers.

    The project is saved in a github repository that contains previously
    fetched/parsed data but no previously trained classifier pickle due to
    size constraints in git.
    REPO: https://github.com/bornandx/nltk_censorship_project.git
