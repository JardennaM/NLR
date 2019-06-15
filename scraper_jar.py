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

termfile = open('terms.txt').readlines()

# Extracts text from website
def url_to_text(url):
    try:
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]
        text = soup.get_text()
        return text.lower()

    except:
        print('failed')


# Does google queries with specified terms, fetches relevant urls and extracts the text.
def search_term(termfile):
    terms = ['drone detection %s'%term.rstrip("\n\r") for term in termfile]
    links = []
    for term in terms:
        for url in search(term, tld="co.in", num=10, stop=10, pause=0.1):
            links.append(url)
    for i in range(len(links)):
        url_to_text(links[i])