import numpy as np
import spacy
import en_core_web_sm
import re
import urllib.request
from bs4 import BeautifulSoup
import extractor
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from nltk.corpus import wordnet

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

terms = {'detection': ['accoustic', 'radio frequency', 'radar', 'camera visual daylight range', 'camera infrared', 
'camera uv', 'camera multi-spectral', 'LIDAR']}


# loading sentences
page = extractor.getPageFromUrl('https://www.l3-droneguardian.com/')
text = extractor.removeScriptAndStyleFromHTML(page)
sentences = extractor.extract_sents(text)
lem_sents = extractor.lemmatize(sentences)
sentences2 = extractor.remove_stopwords_punctuation(lem_sents)

det_sent = []
for s in sentences2:
	det_terms = terms['detection']
	for term in det_terms:
		if term in s:
			det_sent.append(s)
			break
		

print(det_sent)
