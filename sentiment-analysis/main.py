from pprint import pprint
import stanford_nlp
import sentiwordnet_score as swn_score
from tree_method import tree_structure_method
from nltk.tree import *
#from nltk import treetransforms
#from copy import deepcopy


text1 = "There's nothing exactly wrong here, but there's not nearly enough that's right."
text2 = "Not only is entry number twenty the worst of the Brosnan bunch , it's one of the worst of the entire franchise . "
text3 = "Return to Never Land is reliable, standard Disney animated fare, with enough creative energy and wit to entertain all ages ."
text4 = "It 's been done before but never so vividly or with so much passion . "
text5 = "Unfortunately, neither Sendak nor the directors are particularly engaging or articulate ."
text6 = "Flashy gadgets and whirling fight sequences may look cool , but they can't distract from the flawed support structure holding Equilibrium up . "

texts = [text1, text2, text3, text4, text5, text6]

# temp text
#text = "Hello world!  It is so beautiful."
#text = "They haven't succeeded, and will never succeed, in breaking the will of this valiant people"
#text = "The audio system on this television is not very good, but the picture is amazing."
#text = "John is never successful at tennis."
#text = "I really like the toy."
#text = "You are not only tall but also skinny."
#text = "You are neither tall nor skinny."
#text = "I dislike the drink."
#text = "I like the food; I like the drink. "

if __name__ == "__main__":
	# get POS, dependencies
	for text in texts:
		nlp = stanford_nlp.StanfordNLP()
		result = nlp.parse(text)
		#pprint(result)

		parsetree = Tree.fromstring(result['sentences'][0]['parsetree'])
		#print parsetree
		#original = deepcopy(parsetree)
		#treetransforms.un_chomsky_normal_form(original)
		#print original

		senti_score = 0
		senti_score = tree_structure_method(result)

		print "Final Sentiment Score: ", senti_score
		print " \n\n\n\n\n\n\n\n\n "
	










