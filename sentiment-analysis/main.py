from pprint import pprint
import stanford_nlp
import sentiwordnet_score as swn_score
from tree_method import tree_structure_method


# temp text
#text = "Hello world!  It is so beautiful."
text = "I don't hate this movie, it sucks."

if __name__ == "__main__":
	# get POS, dependencies
	nlp = stanford_nlp.StanfordNLP()
	result = nlp.parse(text)
	pprint(result)

	senti_score = 0
	senti_score = tree_structure_method(result)
	print senti_score
	










