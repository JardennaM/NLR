import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
import requests
import time
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

def getTextFromUrl(url):
	"""
	Function extracts HTML from a webpage (or PDF webpage)
	and returns it
	"""

	# if PDF
	try:
		if url[-3:] == 'pdf' or url[-3:] == 'PDF':
			urlretrieve(url, "download.pdf")
			page = convert_pdf_to_txt("download.pdf")
		else:
			page = urllib.request.urlopen(url).read()

		soup = BeautifulSoup(page, 'lxml')
		[s.extract() for s in soup('script')]
		[s.extract() for s in soup('style')]
		text = soup.get_text()
		return text.rstrip("\n\r")
	except:
		return None



def extractSents(text):
	"""
	This function extracts the sentences of a string and returns a list with sentences, 
	tokenized in words.

	"""
	# extract sentences
	sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

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


def getTerms():
	"""
	Gets the terms from the terms.xls file
	"""
	terms = {}

	df = pd.read_excel('terms.xls', index_row=0)
	columnNames = df.columns 

	for name in columnNames:
		terms[name] = []
		for item in df[name]:
			if type(item) != float:
				terms[name].append(item)
	return terms


def flatten(l):
	"""
	Function flattens a sentence and returns the flattened sentence
	"""
	flat_list = []
	for sublist in l:
	    for item in sublist:
	        flat_list.append(item)

	return flat_list


