----------------README----------------------------------------

You will need 2 libraries to run this project 

NLTK: http://www.nltk.org/

TextBlob: https://textblob.readthedocs.io/en/dev/

The scripts should be ran in this order:

	1.) htmlToTxtMaker to fectch the data from the net.
	2.) htmlParser to parse the data.
	3.) htmlClassifier RETRAIN to remake/retrain the pickle.
	4.) htmlClassifier RETRAIN TEST to remake/retrain and test the pickle plus do the user URL input.
	
	NOTE: you can use just htmlClassifier without the retrain if you want to use the latest pickle.
	
	NOTE: htmlClassifier RETRAIN TEST is not ideal to use 
	as the final trained classifier as it won't be trained on all of the data.
	