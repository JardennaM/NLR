import re, math
from collections import Counter
import urllib
import urllib.request
import sys
import operator
import csv
from bs4 import BeautifulSoup
from tabulate import tabulate
import nltk
from nltk.corpus import wordnet
import csv
from cosine_similarity import *
from scraper_jar import *

phases = [['detection', 'detect', 'detector', 'detects', 'detecting'], 
['classification', 'identification', 'classify', 'reaction', 'idenitfy'],
['intent', 'intentionality', 'intention'], ['decision', 'decision support', 'decide'], 
['command', 'control', 'overall', 'main'], 
['intervention', 'intervene', 'interventions', 'neutralisation', 'neutralize', 'neutralise'], 
['forensics']]

classes = ['detection', 'classification', 'identification', 'intent', 'decision', 'command', 'control', 'intervention', 'neutralisation', 'forensics']


with open('keywords.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    keywords_dict = {}
    for row in csv_reader:
        keywords_dict[str(row[0])] = row[1:]
    

def phase_classifier(url, terms):
    text = url_to_text(url)


# with open('../pages/classification/accoustic_4.txt') as f1:
#     url = f1.readline()
#     url = url.split(' ')[1]
#     print(phase_classifier(url, ['main', 'overall']))