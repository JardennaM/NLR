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
import find_terms
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


phases = [['detection', 'detect', 'detector', 'detects', 'detecting', 'recognize'], 
['classification', 'identification', 'classify', 'reaction', 'idenitfy'],
['intent', 'intentionality', 'intention'], 
['decision', 'decision support', 'decide'], 
['command', 'control', 'overall', 'main'], 
['intervention', 'intervene', 'interventions', 'neutralisation', 'neutralize', 'neutralise'], 
['forensics', 'forensic']]

print(np.array(phases).shape)
classes = ['detection', 'classification', 'intent', 'decision', 'command/control', 'intervention/neutralisation', 'forensics']



def determine_terms():
    """ 
        Creates a dictionary with all phases as key and as value their corresponding keywords stored in a list.
    """
    with open('keywords.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        keywords_dict = {}
        for row in csv_reader:
            keywords_dict[str(row[0])] = row[1:]
    return keywords_dict
    
searchterms = ['acoustic', 'frequency', 'frequencies', 'radar', 'infrared camera', 'uv camera', 'multi-spectral camera', 'LIDAR', 'jamming',
'gui', 'method', 'integration', 'architecture', 'capture', 'kinetic', 'datalink jamming', 'gps jamming', 'laser', 'microwave']



# get text by url
url = 'https://www.dronedefence.co.uk/app/uploads/2018/12/SkyFence-brochure-2018121c.pdf'
text = extractor.getTextFromUrl(url)

sentences = extractor.extractSents(text)
worded_text = extractor.flatten(sentences)


# gets the index in the worded_text and the sentence indices
def getSentenceIndex(index, sentences):
	idx_count = -1
	for sent_i, s in enumerate(sentences):
		for j in s:
			idx_count += 1
			if idx_count == index:
				return sent_i



def find_indices_of_terms(search_terms, text, sentences):
	word_indices = [i for i, word in enumerate(text) for term in search_terms if word == term]
	sentence_indices = []
	for i in word_indices:
		sentence_indices.append(getSentenceIndex(i, sentences))
	return word_indices, sentence_indices
    



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
	vec_matrix = [[0, 0, 0, 0 ,0, 0],
				  [0, 0, 0, 0, 0],
				  [0, 0, 0],
				  [0, 0, 0],
				  [0, 0, 0, 0],
				  [0, 0, 0, 0, 0, 0],
				  [0, 0]]

	for word in sur_text:
		for i, phase in enumerate(phases):
			for j, syn in enumerate(phase):
				if word == syn:
					vec_matrix[i][j] += 1
	return np.array(extractor.flatten(vec_matrix))



def cos_sim(a, b):
	if (norm(a)*norm(b)) == 0:
		normv = 0.000000000001
	else:
		normv = (norm(a)*norm(b))
	return dot(a, b)/normv

# Get surrounding text to classify
keyword_indices, sent_indices = find_indices_of_terms(searchterms, worded_text, sentences)


print('Keyword to test:',worded_text[keyword_indices[0]])


# classify with cosine similarity
def get_cosine_sims_classify(index, phases, worded_text, selection):

	surr = surrounding_text(index, worded_text, selection)
	vector = phase_vector(surr, phases)

	
	cosine_sims = []

	for i in range(0, 7):
		zeros = [[0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0],
			 [0, 0, 0],
			 [0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0],
		     [0, 0]]
		zeros[i] = list(np.ones(len(zeros[i])))

		class_vector = np.array(extractor.flatten(zeros))

		cosine_sims.append(cos_sim(vector, class_vector))


	return np.argmax(cosine_sims)
	


# Testing the classification
for index, i in enumerate(keyword_indices):

	key_sent = sentences[sent_indices[index]]
	# remove punctuation from key info, as well as urls
	key_sent = [x for x in key_sent if not x in string.punctuation and not x in ['•', '’', '”', '“', ')', '–', '»', '‘']]

	key = find_terms.getLeastFrequentWords(key_sent, 6)

	print('Key info:', key)
	print('Classified as:', classes[get_cosine_sims_classify(i, phases, worded_text, 20)])
	print('----')





