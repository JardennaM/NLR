import re, math
from collections import Counter
import urllib
import urllib.request
import sys
from urllib.parse import urlparse
import operator
import csv
from bs4 import BeautifulSoup
from tabulate import tabulate
import nltk
from nltk.corpus import wordnet
import csv
from copy import deepcopy
import scraper
import string
import operator
import validators
from validator_collection import validators, checkers
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from numpy import dot
from numpy.linalg import norm
from wordfreq import word_frequency
from input_structure_reader import excel_to_classes_and_searchterms
from scraper import flatten





def find_indices_of_terms(search_terms, sentences):
	"""
	This function, given search terms, return the word indices in de worded_text
	and the sentences indices in the sentence-splitted text for all found search terms.
	"""
	indices = []

	for index, sentence in enumerate(sentences):
		for c, class_terms in enumerate(search_terms):
			for term in class_terms:

				# morgen nog even naar kijken, naar de manier hoe ik dit doe
				if set(term).issubset(set(sentence)):
					if is_term_unique(term, search_terms):
						class_ = c
					else:
						class_ = -1
					indices.append((term, index, class_))

	return indices


def surrounding_text(index, sentences, surr_range):
	"""
	This functions returns the surrounding text given a specific index
	in the sentence-splitted text. The variable surr_range determines
	the range of the sentences you take as context.
	"""
	range_1 = index - surr_range
	range_2 = index + surr_range + 1
	if range_1 >= 0 and range_2 <= len(sentences):
	    return flatten(sentences[range_1:range_2])
	elif range_1 >= 0:
	    return flatten(sentences[range_1:len(sentences)])
	elif range_2 <= len(sentences):
	    return flatten(sentences[0:range_2])
	else:
	    return flatten(sentences[0:len(sentences)])



				
def context_vector(sur_text, classes_vec):
	"""
	Creates a context_vector of the surrounding text of a keyword
	"""
	vec_matrix = create_zeros_list(classes_vec)
	for word in sur_text:
		for i, c in enumerate(classes_vec):
			for j, syn in enumerate(c):
				if word == syn:
					vec_matrix[i][j] += 1
	return np.array(flatten(vec_matrix))

def get_least_frequent_words(sentence, n):
	"""
	Extracts and returns the n least frequent words of a given sentence
	"""
	freq_list = []
	for index, word in enumerate(sentence):
		if is_a_website(word):
			continue
		if word in ['•', '’', '”', '“', ')', '–', '»', '“'] or word in string.punctuation:
			continue
		# make sure frequencies are in there (hardcoded)
		if 'ghz' in word:
			freq_list.append((index, word, 0.0))
		else:
			freq_list.append((index, word, word_frequency(word, 'en')))

	# sort words in least frequency
	sorted_on_freq = [(x[0], x[1]) for x in set(sorted(freq_list, key=lambda tup: tup[2])[0:n])]

	# return list of words in logical order
	return [x[1] for x in sorted(sorted_on_freq, key=lambda tup: tup[0])]

def cos_sim(a, b):
	"""
	Calculats the cosine similarity between two vectors
	"""
	if (norm(a)*norm(b)) == 0:
		normv = 0.000000000001
	else:
		normv = (norm(a)*norm(b))
	return dot(a, b)/normv

def is_a_website(word):
	"""
	Returns True if a word is a website, False otherwise.
	"""
	for element in ['www.', 'http', '.com', '.co']:
		if element in word:
			return True
	return False

def create_zeros_list(listOfLists):
	"""
	Helper function, creates a zeros list of a list of lists
	"""
	mainList = []
	for subList in listOfLists:
		n = len(subList)
		mainList.append([0]*n)
	return mainList

def get_cosine_sims_classify(index, classes_vec, sentences, surr_range):
	"""
	This function classifies a context in the right main category.
	It returns the argmax of the most similar class, using cosine similarity.
	"""


	surr = surrounding_text(index, sentences, surr_range)
	vector = context_vector(surr, classes_vec)

	
	# get cosine sim for each class
	cosine_sims = []
	for i in range(len(classes_vec)-1):
		zeros = create_zeros_list(classes_vec)
		zeros[i] = list(np.ones(len(zeros[i])))
		class_vector = np.array(flatten(zeros))
		cosine_sims.append(cos_sim(vector, class_vector))


	# return class index with highest cosine similarity
	return np.argmax(cosine_sims)
	
def is_term_unique(term, searchterms):
	"""
	This function returns True if a given search term also appears
	in another main category, False otherwise.
	"""
	count = 0
	for term2 in flatten(searchterms):
		if term == term2:
			count += 1
	if count >= 2:
		return False
	else:
		return True

def remove_duplicates(dict_in_dict):
	"""	
	This function removes the duplicates from the dictionary
	created in get_relevant_info
	"""
	for class_, sub in dict_in_dict.items():
		sub2 = []
		for subdict in sub:
			if not subdict in sub2:
				sub2.append(subdict)

		dict_in_dict[class_] = sub2

	return dict_in_dict


# fills dictionary with phase, keywords and keyword info
def get_relevant_info(search_terms, sentences, classes_vec, classes, nFreqWords, surr_range):
	"""
	This function returns combines all functions above and implements the bottom up method.
	It returns a dictionary with the relevant information of the searchterms and their context.
	"""

	sent_indices = find_indices_of_terms(search_terms, sentences)

	main_dict = {}
	for term, index, class_ in sent_indices:


		key_sent = sentences[index]

		# A PRIORI RULES

		# hardcoded, given rule for frequency ghz
		if 'ghz' in key_sent:
			
			j = key_sent.index('ghz')
			if key_sent[j-1].isdigit():
				key_sent[j] = key_sent[j-1] + key_sent[j]
				key_sent.pop(j-1)
			
		# hardcoded, given rule for frequency mhz
		if 'mhz' in key_sent:
			j = key_sent.index('mhz')
			if key_sent[j-1].isdigit():
				key_sent[j] = key_sent[j-1] + key_sent[j]
				key_sent.pop(j-1)

		# --------

		# remove duplicates
		key_sent = list(dict.fromkeys(key_sent))
		# remove punctuation from key info, as well as urls
		key_sent = [x for x in key_sent if not x in string.punctuation and not x in ['•', '’', '”', '“', ')', '–', '»', '‘', '...'] and not is_a_website(x)]

		

		# info to fill dictionary with

		# if not classified, classify (if not unique)
		if class_ == -1:
			c = classes[get_cosine_sims_classify(index, classes_vec, sentences, surr_range)]

		else:
			c = classes[class_]

		key_info = get_least_frequent_words(key_sent, nFreqWords)

		keyword =  ' '.join(term)

		if c not in main_dict.keys():
			main_dict[c] = []
			main_dict[c].append({keyword : [key_info, ' '.join(surrounding_text(index, sentences, surr_range))]})
		else:
			if not {keyword : key_info} in main_dict[c]:
				main_dict[c].append({keyword : [key_info, ' '.join(surrounding_text(index, sentences, surr_range))]})

	main_dict = remove_duplicates(main_dict)

	return main_dict



