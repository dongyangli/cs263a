# CS263 Final Project start code
--------------------------------

# run the project:
	1) Download and configure the python wrapper from https://bitbucket.org/torotoki/corenlp-python
        launch the server:
		cd to corenlp-python folder,
		$python corenlp/corenlp.py
	2) run the code(in another termimnal):
		cd to the sentiment-analysis folder,
		$python main.py

# some explainations on the tree_method algo:
	The parser of StanfordNLP library returns a dictionary of infomation for the input text. (check http://nlp.stanford.edu:8080/parser/ see more details)

	I used the POS tags ('PartOfSpeech') information to find the senti_score of the word if it exists in the sentiwordnet. 

	Negations ('neg') are extracted from the dependencies detected by the parser, check the "Stanford typed dependencies manual" for more details

	The tree structure ('parsetree') of the sentence is used to recursively calculate the overall senti_score of the sentence. 


# note:
	The algorithm is kind of slow now.
	Haven't been tested on any dataset.
