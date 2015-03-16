# Negation Identification and Calculation in Sentiment Analysis
CS263 Final Project
--------------------------------

# How to run the project:
	1) Download and configure the python wrapper from https://bitbucket.org/torotoki/corenlp-python
        launch the server:
		cd to corenlp-python folder,
		$python corenlp/corenlp.py
	2) run the code(in another termimnal):
		cd to the sentiment-analysis folder,
		$python main.py

# Overall algorithm
	
	The whole algorithm is based on the parse tree sturucture returned by the Stanford NLP parser.

	Negations is handled in each node level, which is a partial scope of the whole sentence. 

	The polarity score is calculated from the innermost word/phrase(words or phrase in leaf node of the parse tree) using the sentiwordnet score first. Then in each non-leaf node level, the sentiment score of this level, which is also a scope of the sentence, is determined by the children nodes' score and the existence of negation in current scope. The final score of the root node is used as the sentiment score of the sentence.

# Some clarifications

	Senti-score calculation:
		Senti-score calculation for basic NP/VP phrase:
			Check if there exists 'amod' or 'advmod' dependencies first, if so, use the following equations:
				polarity += (1-noun/adj)(noun/adj)
				polarity += (1-verb/adv)(vb/adv)
			Note the order of using these two equations can't be changed

		Senti-score calculation for single word, noun or verb:
			polarity = sentiwordnet score of word, with its POS tag assigned by Stanford NLP parser

		In the above score calculation process, words of negation such as "not", "never", "neither" and etc are not considered, since it will be handled later in the tree_method.merge() method with the negation rule table.


	Negation identification:
		Negations are detected through the two following sources in tree_method.merge() method:
			(1). The "neg" dependencies returned by Stanford NLP parser.
			(2). Hardcoded negation list that contains "not", "never", "neighter" and etc.

		Source (2) is added since Stanford NLP can't detect "neither" as a negation sign.	



# note:
	The algorithm is kind of slow now.
	Some tested examples:
		"Hello world!  It is so beautiful."
		"They haven't succeeded, and will never succeed, in breaking the will of this valiant people"
		"The audio system on this television is not very good, but the picture is amazing."
		"John is never successful at tennis."
		"I really like the toy."
		"You are neither tall nor skinny."
		"I dislike the drink."
		"I like the food; I like the drink. "
