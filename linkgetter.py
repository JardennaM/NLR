from bs4 import BeautifulSoup
import urllib.request
import re

from bs4 import BeautifulSoup
import urllib.request

def _getLinksFromURL(url):
	resp = urllib.request.urlopen(url)
	soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
	links = []
	for link in soup.find_all('a', href=True):
		if not 'www.' in link:
			links.append(link['href'])
	return links

print(_getLinksFromURL("https://www.reliantemc.com/Aaronia-Drone-Detection-Systems.html"))

