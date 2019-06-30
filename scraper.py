import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
import requests
import time
from nltk import tokenize
from nltk import sent_tokenize
import nltk.data
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from nltk.stem import WordNetLemmatizer 
import pandas as pd
from urllib.request import urlretrieve
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


### MAIN FUNCTIONS

def get_text_from_url(url):
	"""Takes a url as input and returns the text on the specific page as a string.
	Returns False if the text could not be retrieved.

	Parameters:
	url (string): path to website

	Returns:
	text (string): the content on the page or False if the retrieval

	"""
	try:
		# if PDF
		if url[-3:] == 'pdf' or url[-3:] == 'PDF':
			urlretrieve(url, "download.pdf")
			page =  convert_pdf_to_txt("download.pdf")
			os.remove("download.pdf")
		else:
			page = urllib.request.urlopen(url).read()

		soup = BeautifulSoup(page, 'lxml')
		[s.extract() for s in soup('script')]
		[s.extract() for s in soup('style')]
		text = soup.get_text()
		return text.rstrip("\n\r")
	except:
		return False


def extract_sents(text):
	"""
	This function extracts the sentences of a string and returns a list with sentences, 
	tokenized in words.

	"""
	# extract sentences
	sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
	
	# lower senteces
	l_sents = []
	for sent in sentences:
		new_sent = sent.lower()
		tokens = word_tokenize(new_sent)
		l_sents.append(tokens)
	
	return l_sents

def lemmatize(sentences):
	"""
	Function lemmatizes a list of sentences
	"""
	lemmatizer = WordNetLemmatizer()
	lemmatized_sentences = []
	for s in sentences:
		lemmatized_s = []
		for word in s:
			lemmatized_s.append(lemmatizer.lemmatize(word))
		lemmatized_sentences.append(lemmatized_s)

	return lemmatized_sentences


def shorten(sentences):
	"""
	This function removes the punctuation and the stopwords.
	Returns a list of shortened sentences.
	"""
	new_sents = []
	for s in sentences:
		
		# removes stopwords and punctuation
		cleaned = list((set(s) - set(stopwords.words('english'))) - set(string.punctuation))
		if not cleaned == [] and not len(cleaned) < 2 and not len(flatten(cleaned)) < 6:
			new_sents.append(cleaned)


	return new_sents


### HELPER FUNCTIONS

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def flatten(l):
	"""
	Function flattens a sentence and returns the flattened sentence
	"""
	flat_list = []
	for sublist in l:
	    for item in sublist:
	        flat_list.append(item)

	return flat_list


