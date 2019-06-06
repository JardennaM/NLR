import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from googlesearch import search 

termfile = open('terms.txt').readlines()

terms = ['drone detection %s'%term.rstrip("\n\r") for term in termfile]

links = []

for term in terms:
	print(term)
	for j in search(term, tld="co.in", num=10, stop=1, pause=0.1): 
		print(j)
		links.append(j)

for url in links:
	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html)
	text = soup.get_text()
	print(text)
