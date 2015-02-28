from nltk.tree import *
import sentiwordnet_score as swn_score
from pprint import pprint


"""
	find dependencies that contains words
	
	@return: dependencies
"""
def find_dependencies(words, dependencies_list):
	dependencies = []
	for dependency in dependencies_list:
		for word_info in words:
			word = word_info[0]
			#info = word_info[1] #dict, for postages, lemma, etc.
			if word in dependency:
				dependencies.append(dependency)
	return dependencies

"""
	parsetree traversal

	@return: senti_score
"""
def traverse_tree(ptree, words, dependencies):

	senti_score = 0
	if words == 0:
		return senti_score

	try:
		ptree.label()
	except AttributeError:
		return 0

	if ptree.height() == 2:
		senti_score = swn_score.phrase_score(words, find_dependencies(words, dependencies))
		return senti_score

	for subtree in ptree:
		tem_score = traverse_tree(subtree, words, dependencies)
		"""
			To be improved:
			Calculate the senti_score of current node with scores for children nodes
			Simply summed them up now
		"""
		senti_score += tem_score
	return senti_score/len(ptree)

"""
	recursively calculate the score of each subtree of the parsetree, in order to handle
	the negation scope. 

	@return: senti_score
	senti_score > 0 means positive
				< 0 means negtive
"""
def tree_structure_method(result):
	senti_score = 0
	for i, sentence in enumerate(result['sentences']):

		words = sentence['words'] #list
		dependencies = sentence['dependencies'] # list of list
		parsetree = ParentedTree.fromstring(sentence['parsetree'])

		"""
			To be improved:
			The polarity and score of each sentence is calculated based on the 
			parse tree structure
		"""
		score = traverse_tree(parsetree, words, dependencies)


		"""
			define some rule to calculate the overall senti_score based on 
			the polarity and score of each sentence

			I just summed them up here
		"""
		senti_score += score



	print senti_score/len(result)





