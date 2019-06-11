"""
scraper.py

Contains a scraper class with a content property with all the content
from the pages found on the internet based on a file with terms to look for.
"""

import pandas as pd
from googlesearch import search
from bs4 import BeautifulSoup
import urllib.request
import os
import time

class Scraper(object):
	def __init__(self, termsLink, numberOfPagesPerTerm=10, storeLinks=False, storeContent=False):
		self.termsLink = termsLink
		self.numberOfPagesPerTerm = numberOfPagesPerTerm
		self.terms = self.getTerms()
		self.excludedSources = [line.strip('\n') for line in open('excluded_sources.txt').readlines()]
		self.storeContent = storeContent
		if os.path.isfile('links.txt'):
			self.links = self.getLinksFromFile()
		else:
			self.links = self.getLinks(storeLinks)
		self.content = self.getContent()

	def getTerms(self):
		"""Extract the terms from in the specified file and store them
		in a dictionary where the key is the phase"""
		terms = {}

		df = pd.read_excel('%s'%self.termsLink, index_row=0)
		columnNames = df.columns 
		for name in columnNames:
			terms[name] = []
			for item in df[name]:
				if type(item) != float:
					terms[name].append(item)
		return terms

	def getLinks(self, storeLinks):
		"""Return a dictorary of links based on the first N results from
		a google search. Optionaly write these links to a file."""
		file = open('links.txt', 'w')
		totalNumberOfTerms = self.getNumberOfTerms()
		count = 1
		links = {}
		for phase in self.terms:
			links[phase] = {}
			for term in self.terms[phase]:
				links[phase][term] = []
				searchTerm = 'drone %s %s'%(phase, term)
				os.system('clear')
				print('finished searching for %i/%i terms'%(count, totalNumberOfTerms))
				count += 1
				for url in search(searchTerm, tld="co.in", num=self.numberOfPagesPerTerm, stop=self.numberOfPagesPerTerm, pause=2):
					if not self.linkInExclude(url) and not url.endswith('.pdf'):
						links[phase][term].append(url)
						file.write('%s|%s|%s\n'%(phase, term, url))
			time.sleep(5)
		return links

	def downloadPage(self, url):
		"""Returns the content of a page given a url."""
		return urllib.request.urlopen(url).read()

	def getTextFromPage(self, page):
		"""Returns a string with only the html content of a given page."""
		soup = BeautifulSoup(page, 'html')
		[s.extract() for s in soup('script')]
		[s.extract() for s in soup('style')]
		text = soup.get_text()
		return text.rstrip("\n\r")

	def getNumberOfTerms(self):
		"""Returns the total number of terms that need to be googled."""
		count = 0
		for phase in self.terms:
			for term in self.terms[phase]:
				count += 1
		return count

	def getNumberOfLinks(self):
		"""Returns the number of links of the pages that 
		need to be downloaded."""
		count = 0
		for phase in self.links:
			for term in self.links[phase]:
				for link in self.links[phase][term]:
					count += 1
		return count

	def getLinksFromFile(self):
		"""Return a dictionary with the same schema as the getLinks function
		but use the links in the links.txt file instead of googeling them."""
		links = {}
		for phase in self.terms:
			links[phase] = {}
			for term in self.terms[phase]:
				links[phase][term] = []
		file = open('links.txt').readlines()

		for line in file:
			line = line.split('|')
			links[line[0]][line[1]].append(line[2])
		return links

	def getContent(self):
		"""Returns a dictorary with the texts from the content of the links
		in stringform."""
		content = {}
		
		numberOfLinks = self.getNumberOfLinks()
		totalCount = 1
		for phase in self.links:
			content[phase] = {}
			for term in self.links[phase]:
				content[phase][term] = []
				count = 1
				for url in self.links[phase][term]:
					try:
						page = self.downloadPage(url)
						text = self.getTextFromPage(page)
						content[phase][term].append(text)
						os.system('clear')
						print('finished downloading for %i/%i pages'%(totalCount, numberOfLinks))
						totalCount += 1
						if self.storeContent:
							self.storePage(phase, term, text, url, count)
							count += 1
					except:
						pass
		return content

	def storePage(self, phase, method, page, url, index):
		"""Store the text of a page in the correct folder."""
		try:
			os.mkdir('pages')
		except:
			pass
		try:
			os.mkdir('pages/%s'%phase)
		except:
			pass
		file =  open('pages/%s/%s_%i.txt'%(phase, method, index), 'w')
		file.write('url: %s\n'%url)
		file.write(page)
		file.close()

	def linkInExclude(self, link):
		for source in self.excludedSources:
			if source in link:
				return True
		return False
		
		
