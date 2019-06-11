import os
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from googlesearch import search 
import pandas as pd 

os.system('clear')

def getTerms():
	terms = {}

	df = pd.read_excel('terms.xls', index_row=0)
	columnNames = df.columns 

	for name in columnNames:
		terms[name] = []
		for item in df[name]:
			if type(item) != float:
				terms[name].append(item)
	return terms

def getLinks(terms):
	links = []
	for phase in terms:
		for term in terms[phase]:
			counter = 1
			searchTerm = 'drone %s %s'%(phase, term)
			for url in search(searchTerm, tld="co.in", num=10, stop=10, pause=2):
				print(term, url)
				try:
					# links.append('%s %s %s'%(phase, term, url))
					print('link', url)
					page = getPageFromUrl(url)
					print('page')
					cleanedPage = removeScriptAndStyleFromHTML(page)
					print('cleaned')
					storePage(phase, term, cleanedPage, counter)
					print('stored')
					counter += 1
				except:
					print('noop')
	with open('links.txt', 'w') as file:
		for link in links:
			file.write('%s\n'%link)
	return links

def getLinksFromFile():
	links = []
	file = open('links.txt').readlines()
	for link in file:
		links.append(link)
	return links

def getPageFromUrl(url):
	return urllib.request.urlopen(url).read()

def removeScriptAndStyleFromHTML(page):
	soup = BeautifulSoup(page, 'html')
	[s.extract() for s in soup('script')]
	[s.extract() for s in soup('style')]
	text = soup.get_text()
	return text.rstrip("\n\r")

def storePage(phase, method, page, index):
	try:
		os.mkdir('pages')
	except:
		pass
	try:
		os.mkdir('pages/%s'%phase)
	except:
		pass
	file =  open('pages/%s/%s_%i.txt'%(phase, method, index), 'w')
	file.write(page)

terms = getTerms()
# links = getLinks(terms)

def getAndStorePages(links):
	for i in range(len(links)):
		try:
			link = links[i].split()
			phase = link[0]
			method = ' '.join(link[1:-1])
			url = link[-1]
			print(url)
			page = getPageFromUrl(url)
			cleanedPage = removeScriptAndStyleFromHTML(page)
			i += 1
			storePage(phase, method, cleanedPage, i)
		except:
			pass

getLinks(terms)

# for url in links:
# 	page = getPageFromUrl(url)
# 	cleanedPage = removeScriptAndStyleFromHTML(page)
# cleanedPage = removeScriptAndStyleFromHTML(page)

# storePage('detection', 'accoustic', cleanedPage, 1)
