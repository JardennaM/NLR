import numpy as np
import spacy
import en_core_web_sm
import re
import urllib.request
from bs4 import BeautifulSoup
import extractor
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from nltk.corpus import wordnet
from wordfreq import word_frequency
import string
import pandas as pd


### TOP DOWN METHOD TO FIND PHASES AND THEIR KEYWORDS ###

# extracting webpage and loading sentences
url = 'https://phantom-technologies.com/eagle108-drone-detection-jamming-system/'
text = extractor.get_text_from_url(url)
sentences = extractor.extract_sents(text)

# shorten the sentences
#lem_sents = extractor.lemmatize(sentences)
#sentences2 = extractor.shorten(sentences)


phases = [
['detection', 'detect', 'detector', 'detects', 'detecting', 'recognize'], # detection
['classification', 'identification', 'classify', 'identification', 'idenitfy'], # classification
['intent', 'intentionality', 'intention'], # intent
['decision', 'decision support', 'decide'], # decision
['command', 'control', 'overall', 'main'], # command/control
['intervention', 'intervene', 'interventions', 'neutralisation', 'neutralize', 'neutralise'], # intervention
['forensics']] # forensics
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

	# sort words in least frequency
	sorted_on_freq = [(x[0], x[1]) for x in set(sorted(freq_list, key=lambda tup: tup[2])[0:n])]

	# return list of words in logical order
	return [x[1] for x in sorted(sorted_on_freq, key=lambda tup: tup[0])]


def reduceToPhases(phases, sentences):
	"""
	Fills a dictionary with all sentences to corresponding phases.
	Then it reduces those sentences to the least frequent words.
	Returns a dictionary with the phases as keys and the shortened sentences as values
	"""

	# fill dictionary
	dictio = {}
	for phase in phases:
		for syn in phase:
			for s in sentences:
				if syn in s:
					phase_ = str(phase[0])
					if phase_ in dictio:
						if not s in dictio[phase_]:
							dictio[phase_].append(s)
					else: 
						dictio[phase_] = []
						dictio[phase_].append(s)


	# reduce dictionary with least frequent words
	new_dict = {}
	for key, value in dictio.items():
		new_dict[key] = []
		for s in value:
			new_s = getLeastFrequentWords(s, 6)
			# add to dict and remove duplicates
			new_dict[key].append(list(dict.fromkeys(new_s)))
					
	return new_dict
	

## HELPER FUNCTIONS				





# testing
result_dict = reduceToPhases(phases, sentences)

#print('Number of phases filled:', len(result_dict))
import csv

w = csv.writer(open("output.csv", "w"))
for key, val in result_dict.items():
	w.writerow([key])
	for s in val:
		w.writerow([s])


    

