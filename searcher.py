import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from googlesearch import search 
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
from io import BytesIO
from io import StringIO
import os

from extractor import *

def get_systems_from_file(path):
	"""Takes the path to systems.txt as input and returns a list of lists
	where each item constains a manufacturer and a drone system."""
	file = open(path).readlines()

	systems = []
	for line in file[1:]:
		line = line.rstrip('\n').split('|')
		if len(line) == 1:
			systems.append([line[0], ''])
		else:
			systems.append(line)
	return systems

def get_excluded_from_file(path):
	"""Takes the path to excluded.txt as input and returns a list of 
	excluded sources."""
	return [item.rstrip('\n') for item in open(path).readlines()]

def get_searchterms_from_file(path):
	"""Takes the path to search_terms.txt as input and returns a list of 
	search terms."""
	return [item.rstrip('\n') for item in open(path).readlines()]

def site_in_excluded(url, excluded):
	"""Takes a url and a list of excluded sources and returns True if the
	url is in the excluded list. Returns False if it is not in the list."""
	for site in excluded:
		if site in url:
			return True
	return False

def create_search_terms_list(systems, searchterms):
	to_search = []
	for system in systems:
		system_list = []
		if system[1] != '':
			for term in searchterms:
				system_list.append(system[0] + ' ' + system[1] + ' ' + term)
				#system_list.append(system[1] + ' ' + term)
		[to_search.append(item) for item in system_list]
	return to_search

def google_terms(searchterms, excluded, number_of_urls_per_term=25):
	"""Given a list of search terms and a list of excluded sources
	it returns a list of urls returned by a google search. By default
	the number of urls returned per searchterm is 25 but this can be 
	altered by an extra input argument.""" 
	urls = []

	count = 0
	number_of_searchterms = len(searchterms)
	while count < number_of_searchterms:
		print(count, 'van de', number_of_searchterms)
		term = searchterms[count]
		try:
			for url in search(term, tld="co.in", num=25, stop=10, pause=1):
				if not site_in_excluded(url, excluded):
					# print(term.split()[:-1])
					urls.append('%s|%s'%(' '.join(term.split()[:-1]),url))
			count += 1
		except:
			print('wait')
			time.sleep(900)

	with open('results/urls.txt', 'w') as file:
		for url in urls:
			file.write('%s\n'%url)
	file.close()
	return urls

def read_urls_from_file(path):
	urls = []
	for line in open(path).readlines():
		if not line.startswith('>>>') and not line.startswith('<<<'):
			line = line.rstrip('\n').split('|')
			urls.append([line[0], line[1]])
	return urls

def write_page_to_file(text, url, term):
	try:
		os.mkdir('results/pages')
	except:
		pass
	try:
		os.mkdir('results/pages/%s-%s'%(manufacturer, system))
	except:
		pass
	try:
		index = max([filename.split('.')[0]])
	except:
		index = 1
	file = open('results/pages/%s/%i.txt'%(term, index), 'w')
	file.write('%s\n'%url)
	file.write(text)
	file.close()

def getTextFromUrl(url):
	"""
	Function extracts HTML from a webpage (or PDF webpage)
	and returns it
	"""

	# if PDF
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
# systems = get_systems_from_file('data/drone_systems.txt')
# excluded = get_excluded_from_file('data/excluded.txt')
# searchterms = get_searchterms_from_file('data/search_terms.txt')
# searchterm_list = create_search_terms_list(systems, searchterms)[:5]

# urls = google_terms(searchterm_list, excluded)

urls = read_urls_from_file('results/urls.txt')
for url in urls[2:]:
	os.system('clear')
	print('url', url[1])
	text = getTextFromUrl(url[1])


