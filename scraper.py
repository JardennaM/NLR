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
from urllib.request import urlretrieve
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def get_text_from_url(url):
	"""Takes a url as input and returns the text on that page as output.

	Paramters:
	url (string): link to a webpage

	Returns:
	content (string): the text from the webpage

	"""
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

def convert_pdf_to_txt(path):
	"""Takes the path to a PDF file as input and returns the text that is on 
	the page.

	Parameters:

	Returns:


	"""
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

def extractSents(text):
	"""
	This function extracts the sentences of a string and returns a list with sentences, 
	tokenized in words.
	"""
	# extract sentences
	sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

	# lower senteces
	sentences_list = []
	for sentence in sentences:
		sentence = sentence.lower()
		tokens = word_tokenize(sentence)
		sentences_list.append(tokens)
	
	return sentences_list

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

def flatten(lst):
	"""
	Function flattens a sentence and returns the flattened sentence
	"""
	flattend_list = []
	for sublist in lst:
	    for item in sublist:
	        flattend_list.append(item)

	return flattend_list

def shorten(sentences):
	"""This function removes the punctuation and the stopwords.
	Returns a list of shortened sentences.
	"""
	new_sentence = []
	for sentence in sentences:
		
		# removes stopwords and punctuation
		cleaned = list((set(sentence) - set(stopwords.words('english'))) - set(string.punctuation))
		if not cleaned == [] and not len(cleaned) < 2 and not len(flatten(cleaned)) < 6:
			new_sentence.append(cleaned)
	return new_sentence

def extract_cleaned_sentences(text):
	sentences = extractSents(text)
	lemmatized = lemmatize(sentences)
	shortened = shorten(lemmatized)
	return shortened


