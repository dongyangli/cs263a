from nltk.corpus import wordnet as wn
import mr_bag_of_words as mr_bow
from pprint import pprint
from nltk.corpus import sentiwordnet as swn

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
	("NN", 'n'), ("NNS", 'n'), ("NNP", 'n'), ("NNPS", 'n'), \
	("RB", 'r'), ("RBR", 'r'), ("RBS", 'r'), \
	("VB", 'v'), ("VBD", 'v'), ("VBG", 'v'),("VBN", 'v'), ("VBP", 'v'), ("VBZ", 'v')])



"""
	used in the paper_method

	@return pos, neg
	The senti_score of the word in sentiwordnet
"""
def word_senti_score(word, penn_pos, neg_dependencies):
	
	pos = neg = 0
	if POS_tags.has_key(penn_pos):
		nltk_pos = POS_tags[penn_pos]
		word_senti_synsets = swn.senti_synsets(word, nltk_pos)
	else:
		word_senti_synsets = swn.senti_synsets(word)

	for word_senti in word_senti_synsets:
		"""
			Here the pos_score()/neg_score() returned is the possibility of the word 
			to be positive/negtive 
		"""
		pos += word_senti.pos_score()
		neg += word_senti.neg_score()
	if(len(word_senti_synsets) > 0):
		pos = pos/len(word_senti_synsets)
		neg = neg/len(word_senti_synsets)

	"""
		use the dependencies to check negation
		if there is negation associated with the word, reverse 
		its pos_score and neg_score simply
	"""
	for dependency in neg_dependencies:
		if word in dependency:
			pos, neg = neg, pos # reverse polarity value

	return pos, neg 

"""
	@return neg_dependencies
"""
def get_neg_dependencies(dependencies):
	neg_dependencies = []
	for dependency in dependencies:
		if dependency[0] == 'neg':
			neg_dependencies.append(dependency)
	return neg_dependencies

"""
	used in tree_structure_method

	@return senti_score
"""
def phrase_score(text, dependencies = None):

	neg_dependencies = get_neg_dependencies(dependencies)
	senti_score = 0
	pos = neg = 0
	if text == 0:
		return senti_score

	for word_info in text:
		word = word_info[0]
		info = word_info[1] #dict
		penn_pos = info['PartOfSpeech']
		w_pos, w_neg = word_senti_score(word, penn_pos, neg_dependencies)
		"""
			To be done: 
				calculte the phrase score with help of dependencies or sth
		"""
		pos += w_pos
		neg += w_neg

	if pos > neg:
		senti_score = pos/len(text)
	else:
		senti_score = -neg/len(text)

	return senti_score
	









