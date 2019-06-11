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
	print('term', term)
	for url in search(term, tld="co.in", num=10, stop=10, pause=0.1):
		links.append(url)

for i in range(len(links)):
	try:
		url = links[i]

		file = open('%s.txt'%i, 'w')
		file.write('This information is from %s\n\n'%url)
		html = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html, parser='html')
		[s.extract() for s in soup('script')]
		[s.extract() for s in soup('style')]
		text = soup.get_text()
		# lines = [line.strip() for line in text.splitlines()]
		file.write(text)
		file.close()
	except:
		print('noop')