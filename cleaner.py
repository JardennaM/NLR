import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from googlesearch import search 
from nltk import sent_tokenize
import nltk.data
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

def flatten(l):
	flat_list = []
	for sublist in l:
	    for item in sublist:
	        flat_list.append(item)

	return flat_list

def extract_sents(txtfile):
	"""
	This function extract the sentences of a txt file and return a list with sentences, 
	tokenized in words.
	"""
	with open(txtfile) as f:
		text = f.read()

	# extract sentences
	sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

	# lower senteces
	l_sents = []
	for sent in sentences:
		new_sent = sent.lower()
		tokens = word_tokenize(new_sent)
		l_sents.append(tokens)
	
	return l_sents


def remove_stopwords_punctuation(sentences):
	"""
	This function removes the punctuation and the stopwords.
	Returns a list of sentences.
	"""
	new_sents = []
	for s in sentences:
		
		# removes stopwords and punctuation
		cleaned = list((set(s) - set(stopwords.words('english'))) - set(string.punctuation))
		if not cleaned == [] and not len(cleaned) < 2 and not len(flatten(cleaned)) < 6:
			new_sents.append(cleaned)


	return new_sents


# testing
txtfile = 'pages/classification/accoustic_5.txt'
sentences = extract_sents(txtfile)

#sentences = remove_stopwords_punctuation(sentences)


for s in sentences:
	if 'accoustic' in s or 'detection' in s:
		print(s)




