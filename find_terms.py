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


terms = extractor.getTerms()

# extracting webpage and loading sentences
text = extractor.getTextFromUrl('https://www.hensoldt.net/fileadmin/hensoldt/Datenbl%C3%A4tter/0779_17_Xpeller_brochure_E_for_Email.pdf')
sentences = extractor.extractSents(text)
lem_sents = extractor.lemmatize(sentences)
sentences2 = extractor.shorten(lem_sents)


dictio = {}

phases = [['detect', 'detector', 'detects', 'detecting', 'detection']]

for phase in phases:
	idx = 0
	for syn in phase:
		for s in sentences2:
			if syn in s:
				idx += 1
				stringo = str('detection') + ' ' + str(idx)
				dictio[stringo] = s
					
		
print(dictio)
