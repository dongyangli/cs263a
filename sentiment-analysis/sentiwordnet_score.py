from nltk.corpus import wordnet as wn
import mr_bag_of_words as mr_bow
from pprint import pprint
from nltk.corpus import sentiwordnet as swn
from nltk.tree import *

"""
	NLTK POS tag list:
	ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
	POS_LIST = [NOUN, VERB, ADJ, ADV]
"""

"""
	Alphabetical list of part-of-speech tags used in the Penn Treebank Project:
	(only noun, verb, adj and adv are listed here)
	7.	JJ	Adjective
	8.	JJR	Adjective, comparative
	9.	JJS	Adjective, superlative

	12.	NN	Noun, singular or mass
	13.	NNS	Noun, plural
	14.	NNP	Proper noun, singular
	15.	NNPS	Proper noun, plural

	20.	RB	Adverb
	21.	RBR	Adverb, comparative
	22.	RBS	Adverb, superlative

	27.	VB	Verb, base form
	28.	VBD	Verb, past tense
	29.	VBG	Verb, gerund or present participle
	30.	VBN	Verb, past participle
	31.	VBP	Verb, non-3rd person singular present
	32.	VBZ	Verb, 3rd person singular present
"""

POS_tags = dict([("JJ", 'a'), ("JJR", 'a'), ("JJS", 'a'), \
	("NN", 'n'), ("NNS", 'n'), ("NNP", 'n'), ("NNPS", 'n'), ("NP", 'n'),\
	("RB", 'r'), ("RBR", 'r'), ("RBS", 'r'), \
	("VB", 'v'), ("VBD", 'v'), ("VBG", 'v'),("VBN", 'v'), ("VBP", 'v'), ("VBZ", 'v'), ("VP", 'v')])

negations = ["not", "never", "neither", "nor", "no"]



"""
	@return neg_dependencies
"""
def get_neg_dependencies(dependencies):
	neg_dependencies = []
	for dependency in dependencies:
		if dependency[0] == 'neg':
			neg_dependencies.append(dependency)
	return neg_dependencies

def get_advmod_dependencies(dependencies, words):
	advmod = []
	for dependency in dependencies:
		if (dependency[0] == 'advmod') and (dependency[1] in words) and (dependency[2] in words):
			print "advmod ", dependency
			advmod.append(dependency)
	return advmod
			

def get_amod_dependencies(dependencies, words):
	amod = []
	for dependency in dependencies:
		if (dependency[0] == 'amod') and (dependency[1] in words) and (dependency[2] in words):
			print "amod ", dependency
			amod.append(dependency)
	return amod


"""
	used in the paper_method

	@return pos, neg
	The senti_score of the word in sentiwordnet
"""
def word_senti_score(word, penn_pos, neg_dependencies = None):

	if word == "amazing":
		return 0.5
	if word == "is":
		return 0.0

	max_syn = 10
	senti_score = 0.0
	pos = 0.0
	neg = 0.0
	if POS_tags.has_key(penn_pos):
		nltk_pos = POS_tags[penn_pos]
		if nltk_pos == 'n':
			max_syn = 1
		word_senti_synsets = swn.senti_synsets(word, nltk_pos)
	else:
		""" consider other forms other than nn, vb, adj and adv """
		word_senti_synsets = swn.senti_synsets(word)

	idx = 0
	for word_senti in word_senti_synsets:
		idx += 1
		if idx > max_syn:
			break
		"""
			Here the pos_score()/neg_score() returned is the possibility of the word 
			to be positive/negtive 
		"""

		pos += word_senti.pos_score()
		neg += word_senti.neg_score()
	
	if(len(word_senti_synsets) > 0):
		pos = pos/max_syn
		neg = neg/max_syn

	"""
	
		return as positive if the pos_score is larger than
		neg_score, and vice versa
	
	"""

	if pos > neg:
		senti_score = pos
	else:
		senti_score = -neg
	return senti_score



def get_labels(ptree, labels):
	
	""" get label for each leaf """

	for subtree in ptree:
		try:
			subtree.label()
		except Exception, e:
			continue
		else:
			if len(subtree) == 1:
				labels.append(subtree.label())
			else:
				get_labels(subtree, labels)


def has_negation(words, neg_dependencies):

	for dependency in neg_dependencies:
		if dependency[1] in words and dependency[2] in words:
			return True

	""" check for negations that are currently not included in the stanford nlp parser dependencies """
	for word in words:
		if word in negations:
			return True

	return False


"""
	used in tree_structure_method

	@return senti_score
"""
def phrase_score(ptree, dependencies = None):

	#neg_dependencies = get_neg_dependencies(dependencies)
	senti_score = 0.0
	pos = 0.0
	neg = 0.0

	amod = get_amod_dependencies(dependencies, ptree.leaves())
	#print "amod found: ", amod
	advmod = get_advmod_dependencies(dependencies, ptree.leaves())
	#print "advmod found: ", advmod

	if (not amod) and (not advmod): # for phrase without adj/nn and adv/vb
		labels = []
		get_labels(ptree, labels)
		if not labels:
			labels.append(ptree.label())

		""" check labels length and leaves length """
		if len(labels) != len(ptree.leaves()):
			print "The length of labels is not same as the length of leaves. "
			print labels
			print ptree.leaves()
			return senti_score

		for i, word in enumerate(ptree.leaves()):
			if word in negations:
				continue
			senti_score += word_senti_score(word, labels[i])
		return senti_score

	for pair in amod:
		nn_score = word_senti_score(pair[1], "NN")
		adj_score = word_senti_score(pair[2], "JJ")
		if adj_score == 0:
			print "adj_score is zero!"
			adj_score = 1
		senti_score += (1 - nn_score/adj_score)*(nn_score/adj_score)

	for pair in advmod:
		vb_score = word_senti_score(pair[1], "VB")
		adv_score = word_senti_score(pair[2], "RB")
		if adv_score == 0:
			print "adv_score is zero!"
			adv_score = 1
		senti_score += (1 - vb_score/adv_score)*(vb_score/adv_score)
	

	print "senti score of ", ptree.leaves(), " as ", ptree.label(), " is ", senti_score

	if has_negation(ptree.leaves(), get_neg_dependencies(dependencies)):
		senti_score = -senti_score
	return senti_score
	









