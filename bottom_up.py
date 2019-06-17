import re, math
from collections import Counter
import urllib
import urllib.request
import sys
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

phases = [['detection', 'detect', 'detector', 'detects', 'detecting'], 
['classification', 'identification', 'classify', 'reaction', 'idenitfy'],
['intent', 'intentionality', 'intention'], ['decision', 'decision support', 'decide'], 
['command', 'control', 'overall', 'main'], 
['intervention', 'intervene', 'interventions', 'neutralisation', 'neutralize', 'neutralise'], 
['forensics']]

classes = ['detection', 'classification', 'identification', 'intent', 'decision', 'command', 'control', 'intervention', 'neutralisation', 'forensics']


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
    
searchterms = ['acoustic', 'frequency', 'frequencies', 'radar', 'infrared camera', 'uv camera', 'multi-spectral camera', 'LIDAR', 'jamming']




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

				
def freq_of_words(sur_text, search_terms):
    overlapping_words = set(sur_text) & set(search_terms)
    word_freqs = Counter(sur_text)
    freq_dict = {}
    for word in overlapping_words:
        freq_dict[word] = word_freqs[word]
    return freq_dict



# Get surrounding text to classify
keyword_indices, sent_indices = find_indices_of_terms(searchterms, worded_text, sentences)
print(keyword_indices, sent_indices)


surr = surrounding_text(keyword_indices[0], worded_text, 20)

# remove punctuation from surrounding text
surr = [x for x in surr if not x in string.punctuation]
	

# now I want the keyword info from the sentence it is in

key_surr = surrounding_text(keyword_indices[0], worded_text, 5)	

key = find_terms.getLeastFrequentWords(key_surr, 6)

print(worded_text[keyword_indices[0]])
print(key_surr)
print(key)


