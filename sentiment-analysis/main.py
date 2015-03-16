from pprint import pprint
import stanford_nlp
import sentiwordnet_score as swn_score
from tree_method import tree_structure_method
from nltk.tree import *
#from nltk import treetransforms
#from copy import deepcopy



# temp text
#text = "Hello world!  It is so beautiful."
text = "They haven't succeeded, and will never succeed, in breaking the will of this valiant people"
#text = "The audio system on this television is not very good, but the picture is amazing."
#text = "John is never successful at tennis."
text = "I really like the toy."
#text = "You are not only tall but also skinny."
text = "You are neither tall nor skinny."
#text = "I dislike the drink."
#text = "I like the food; I like the drink. "

if __name__ == "__main__":
	# get POS, dependencies
	nlp = stanford_nlp.StanfordNLP()
	result = nlp.parse(text)
	pprint(result)

	parsetree = Tree.fromstring(result['sentences'][0]['parsetree'])
	print parsetree
	#original = deepcopy(parsetree)
	#treetransforms.un_chomsky_normal_form(original)
	#print original

	senti_score = 0
	senti_score = tree_structure_method(result)
	print senti_score
	










