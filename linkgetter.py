from bs4 import BeautifulSoup
import urllib.request
import re
import os
from urllib.parse import urlparse

def _getLinksFromURL(url, allLinks):
	resp = urllib.request.urlopen(url)
	soup = BeautifulSoup(resp, 'html', from_encoding=resp.info().get_param('charset'))
	links = soup.find_all('a', href=True)
	if len(links) == 0:
		return allLinks + links
	for link in soup.find_all('a', href=True):
		if not 'www.' in link and link not in links:
			try:
				print(link)
				link = 'http://' + urlparse(url).netloc + '/' + link['href']
				allLink.append(_getLinksFromURL(link, allLinks))
			except:
				pass
	return allLink

def getLinksFromURL(url):
	allLinks = [url]
	resp = urllib.request.urlopen(url)
	soup = BeautifulSoup(resp, 'html', from_encoding=resp.info().get_param('charset'))
	for link in soup.find_all('a', href=True):
		if not 'www.' in link:
			try:
				link = 'http://' + urlparse(url).netloc + '/' + link['href']
				# print(link)
				allLinks.append(_getLinksFromURL(link, allLinks))
			except:
				pass
	return allLinks
		

print(getLinksFromURL("http://cstwiki.wtb.tue.nl/index.php?title=System_Architecture_Robotic_Drone_Referee"))


