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
import extractor
import string
import operator
import validators
from validator_collection import validators, checkers
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from numpy import dot
from numpy.linalg import norm
from wordfreq import word_frequency
import scraper


# gets the index in the worded_text and the sentence indices
def getSentenceIndex(index, sentences):
	idx_count = -1
	for sent_i, s in enumerate(sentences):
		for j in s:
			idx_count += 1
			if idx_count == index:
				return sent_i

def flatten(l):
	"""
	Function flattens a sentence and returns the flattened sentence
	"""
	flat_list = []
	for sublist in l:
	    for item in sublist:
	        flat_list.append(item)

	return flat_list


def find_indices_of_terms(search_terms, text, sentences):
	"""
	This function, given search terms, return the word indices in de worded_text
	and the sentences indices in the sentence-splitted text for all found search terms.
	"""
	word_indices = [i for i, word in enumerate(text) for term in search_terms if word == term]
	sentence_indices = []
	for i in word_indices:
		sentence_indices.append(getSentenceIndex(i, sentences))
	return word_indices, sentence_indices
    

# gets surrounding text with selection parameter around keyword in text
def surrounding_text(index, text, selection):
    range_1 = index - selection
    range_2 = index + selection + 1
    if range_1 >= 0 and range_2 <= len(text):
        return text[range_1:range_2]
    elif range_1 >= 0:
        return text[range_1:len(text)]
    elif range_2 <= len(text):
        return text[0:range_2]
    else:
        return text[0:len(text)]

				
def phase_vector(sur_text, phases):
	"""
	Creates a phase_vector of the surrounding text of a keyword
	"""
	vec_matrix = createZerosList(phases)

	for word in sur_text:
		for i, phase in enumerate(phases):
			for j, syn in enumerate(phase):
				if word == syn:
					vec_matrix[i][j] += 1
	return np.array(extractor.flatten(vec_matrix))

def getLeastFrequentWords(sentence, n):
	"""
	Extracts and returns the n least frequent words of a given sentence
	"""
	freq_list = []
	for index, word in enumerate(sentence):
		
		if word in ['•', '’', '”', '“', ')', '–', '»'] or word in string.punctuation:
			continue
		# make sure frequencies are in there (hardcoded)
		if 'ghz' in word:
			freq_list.append((index, word, 0.0))
		else:
			freq_list.append((index, word, word_frequency(word, 'en')))

	print('freqs', freq_list)
	# sort words in least frequency
	sorted_on_freq = [(x[0], x[1]) for x in set(sorted(freq_list, key=lambda tup: tup[2])[0:n])]

	# return list of words in logical order
	return [x[1] for x in sorted(sorted_on_freq, key=lambda tup: tup[0])]

def cos_sim(a, b):
	if (norm(a)*norm(b)) == 0:
		normv = 0.000000000001
	else:
		normv = (norm(a)*norm(b))
	return dot(a, b)/normv

def wordNotFiltered(word):
	filters = ['www.', '.com', 'http']
	for element in filters:
		if element in word:
			return False
	return True

def createZerosList(listOfLists):
	"""
	Helper function, creates a zeros list of a list of lists
	"""
	mainList = []
	for subList in listOfLists:
		n = len(subList)
		mainList.append([0]*n)
	return mainList


# classify with cosine similarity
def get_cosine_sims_classify(index, phases, worded_text, selection):

	surr = surrounding_text(index, worded_text, selection)
	vector = phase_vector(surr, phases)

	
	# get cosine sim for each class
	cosine_sims = []
	for i in range(0, 7):
		zeros = createZerosList(phases)
		zeros[i] = list(np.ones(len(zeros[i])))
		class_vector = np.array(extractor.flatten(zeros))
		cosine_sims.append(cos_sim(vector, class_vector))


	# return class index with highest cosine similarity
	return np.argmax(cosine_sims)
	

# fills dictionary with phase, keywords and keyword info
def fillDict(searchterms, sentences, worded_text, phases, classes, nFreqWords, nSelection):
	"""
	PARAMS
	searchterms: keywords that will be searched in the text
	sentences: the text splitted in sentences
	worded_text: the text splittted in words
	phases: list of (synonyms) of phases
	classes: simple list of phases/classes
	nFreqWords: number of freq to shorten sentence
	nSelection: number of surroundings to use around keywords
	"""

	keyword_indices, sent_indices = find_indices_of_terms(searchterms, worded_text, sentences)
	main_dict = {}
	for index, i in enumerate(keyword_indices):

		key_sent = sentences[sent_indices[index]]

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

		# remove punctuation from key info
		key_sent = [x for x in key_sent if not x in string.punctuation and not x in ['•', '’', '”', '“', ')', '–', '»', '‘', '...']]


		# info to fill dictionary with
		phase = classes[get_cosine_sims_classify(i, phases, worded_text, nSelection)]

		key_info = getLeastFrequentWords(key_sent, nFreqWords)

		print(key_sent, key_info)
		keyword =  worded_text[i]

		if phase not in main_dict.keys():
			main_dict[phase] = []
			main_dict[phase].append({keyword : key_info})
		else:
			if not {keyword : key_info} in main_dict[phase]:
				main_dict[phase].append({keyword : key_info})

	return main_dict