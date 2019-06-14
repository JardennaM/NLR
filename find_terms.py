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

### TOP DOWN METHOD TO FIND TERMS AND ATTRIBUTES ###

terms = extractor.getTerms()

# extracting webpage and loading sentences
text = extractor.getTextFromUrl('https://www.accipiterradar.com/products/safety/drone-uav-detection-tracking-alerting/')
sentences = extractor.extractSents(text)
# shorten the sentences
#lem_sents = extractor.lemmatize(sentences)
#sentences2 = extractor.shorten(sentences)



dictio = {}

phases = [['detection', 'detect', 'detector', 'detects', 'detecting'], ['classification', 'identification', 'classify', 'identification', 'idenitfy'],
['intent', 'intentionality', 'intention'], ['decision', 'decision support', 'decide'], ['command', 'control', 'overall', 'main'], 
['intervention', 'intervene', 'interventions', 'neutralisation', 'neutralize', 'neutralise', 'frequency', 'frequencies'], ['forensics']]

for phase in phases:
	idx = 0
	for syn in phase:
		for s in sentences:
			if syn in s:
				idx += 1
				stringo = str(phase[0]) + ' ' + str(idx)
				dictio[stringo] = s
					
		
#for key, value in dictio.items():
	#print(key, value)


def getLeastFrequentWords(sentence):
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
	sorted_on_freq = [(x[0], x[1]) for x in set(sorted(freq_list, key=lambda tup: tup[2])[0:5])]

	# return list of words in logical order
	return [x[1] for x in sorted(sorted_on_freq, key=lambda tup: tup[0])]

for key in dictio.keys():
	print(key, ':', getLeastFrequentWords(dictio[key]))


