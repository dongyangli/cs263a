from nltk.tree import *
import sentiwordnet_score as swn_score
from pprint import pprint

punctuation_marks = [",", ".", ";", "\"", "\'", "~"]
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
	@return neg_dependencies
"""
def get_neg_dependencies(dependencies):
	neg_dependencies = []
	for dependency in dependencies:
		if dependency[0] == 'neg':
			neg_dependencies.append(dependency)
	return neg_dependencies



def is_leaf_phrase(ptree):
	for subtree in ptree:
		try:
			subtree.label()
		except Exception, e:
			continue 
		else:
			#print "in is_leaf_phrase now:"
			#print subtree.leaves(), subtree.label()
			if(subtree.label() == "VP" or subtree.label() == "NP" or is_leaf_phrase(subtree)):
				return False

			
	return True

def polarity(first, second, has_negation = False):
	polarity =  abs(first) + (1 - abs(second))*abs(second)
	# table used here 
	if first >= 0 and second >= 0 and has_negation:
		return -polarity
	elif first >= 0 and second >= 0 and not has_negation:
		return polarity
	elif first >= 0 and second < 0 and has_negation:
		return polarity
	elif first >= 0 and second < 0 and not has_negation:
		return -polarity
	elif first < 0 and second >= 0 and has_negation:
		return polarity
	elif first < 0 and second >= 0 and not has_negation:
		return -polarity
	elif first < 0 and second < 0 and has_negation:
		return -polarity
	elif first < 0 and second < 0 and not has_negation:
		return polarity
	else:
		return first + (1 - second)*second


def merge(children_scores, children_leaves, neg_dependencies):
	
	length = len(children_scores)
	print "in merging ", children_scores
	if length == 0:
		return 0.0
	if length == 1:
		return children_scores[0]


	""" 
		check any word in these phrase is marked in negation dependencies 
		here, using the children_leaves list 
	"""
	second_phrase = children_leaves.pop()
	first_phrase = children_leaves.pop()
	children_leaves.append(first_phrase.append(second_phrase))
	has_negation = False
	for dependency in neg_dependencies:
		if (dependency[1] in first_phrase and dependency[2] in second_phrase)\
		or (dependency[2] in first_phrase and dependency[1] in second_phrase):
			has_negation = True
	""" check for negations that are currently not included in the stanford nlp parser dependencies """
	for word in first_phrase:
		if word in swn_score.negations:
			has_negation = True


	""" 
		calculate score 
	"""
	second_score = children_scores.pop()
	first_score = children_scores.pop()
	children_scores.append(polarity(first_score, second_score, has_negation))

	""" 
		keeping merging 
	"""
	return merge(children_scores, children_leaves, neg_dependencies)


def conjunction_merge(children_scores, children_labels, children_leaves):
	""" find CC first, then combine it with its left and right neighbors """
	""" from right to left """
	for i, pos in enumerate(children_labels):
		if pos == "CC":
			""" and, but, or, etc. """
			""" other rules could be added here later """
			print "when pos is CC ", children_leaves[i][0], " conjunction merging ... "
			if children_leaves[i][0] == "and" or children_leaves[i][0] == "or": # children_leaves[i][0] in conc_same:
				children_scores[i-1] += children_scores.pop(i) + children_scores.pop(i)
			else: # " but " # children_leaves[i][0] in conc_contrast:
				children_scores[i-1] *= 0.2
				children_scores[i-1] += children_scores.pop(i) + 1.8*children_scores.pop(i)
			children_labels.pop(i)
			children_labels.pop(i)

			""" pop out the conjunction word """
			children_leaves.pop(i)
			""" combine the two sides of conjunction word together """
			children_leaves[i-1].append(children_leaves.pop(i))
			



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
	else:
		
		if ptree.height() == 2:
			print " "
			print " -------- leaf node --------- "
			print ptree.label()
			print "node: ", ptree.leaves()
			print " -------- leaf node --------- "
			
			

			senti_score = swn_score.phrase_score(ptree, dependencies)
			print "the score of leaf node is ", senti_score
			print " "
			return senti_score
		
		if (ptree.label() == "VP" or ptree.label() == "NP") and is_leaf_phrase(ptree): 
			""" is_leaf_phrase means no more VP or NP children in this ptree """
			
			print " "
			print " -------- leaf phrase --------- "
			print ptree.label()
			print "node: ", ptree.leaves()
			print " -------- leaf phrase --------- "
			#print " "

			#print ptree.label(), ptree.leaves()
			print "number of children is ", len(ptree), ", root label: ", ptree.label()
			
			
			senti_score = swn_score.phrase_score(ptree, dependencies)
			if senti_score is None:
				print "phrase_score is None!"
			print "the score of leaf phrase is ", senti_score
			print " "
			return senti_score



		"""
		print " "
		print " -------- nonleaf phrase --------- "
		print ptree.label()
		print "node: ", ptree.leaves()
		print " -------- nonleaf phrase --------- "
		print " "
		"""
		children_scores = []
		children_labels = []
		children_leaves = []
		for child in ptree:
			#if (ptree.label() == "VP" or ptree.label() == "NP"):
				#print "child of ",  ptree.leaves(), " :      ", child.label(), child.leaves()
			try:
				child.label()
			except Exception, e:
				continue
			else:

				if (child.label()) in punctuation_marks:
					continue

				tem_score = traverse_tree(child, words, dependencies)
				if tem_score == None:
					print "None detected!"
					print "child is ", child.leaves()
					continue
				children_scores.append(tem_score)
				children_labels.append(child.label())
				children_leaves.append(child.leaves())

		"""
		if ptree contains negation:
			senti_score = -senti_score 

		apply the first/second equation:
		first + [(1 - second)*second]
		"""
		print " "
		print "-----------------------------------------------------"
		print ptree.leaves()
		print "before merging ", children_scores
		conjunction_merge(children_scores, children_labels, children_leaves)



		senti_score = merge(children_scores, children_leaves, get_neg_dependencies(dependencies))
		print "senti_score returned from merge ", senti_score
		print "-----------------------------------------------------"
		print " "
		return senti_score


"""
	recursively calculate the score of each subtree of the parsetree, in order to handle
	the negation scope. 

	@return: senti_score
	senti_score > 0 means positive
				< 0 means negtive
"""
def tree_structure_method(result):
	senti_score = 0
	idx = 0
	for sentence in result['sentences']:

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
			the polarity and score of each SENTENCE

			I just summed them up here
		"""
		senti_score += score



	print senti_score/len(result)





