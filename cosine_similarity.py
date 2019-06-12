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
from scraper_jar import *


WORD = re.compile(r'\w+')


# Determines the cosine similarity.
def determine_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[x] * vec2[x] for x in intersection)
    
    length_1 = sum([vec1[x]**2 for x in vec1.keys()])
    length_2 = sum([vec2[x]**2 for x in vec2.keys()])
    
    denominator = math.sqrt(length_1) * math.sqrt(length_2)
    
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# Returns a set of the lemma's and synonyms of a word.
def find_synset(term):
    synsets = wordnet.synsets(term)
    synonyms = [l.name() for syn in synsets for l in syn.lemmas()]
    return set(synonyms)

# Vectorizes the text and creates a dictionary with the word as key and
# the frequencie as value.
def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

# Finds synomyms of a term and creates a dictionary with
# as value the frequencies.
def term_vector(terms):
    term_vec = {}
    for term in terms:
        set1 = Counter(find_synset(term))
        term_vec = merge_two_dicts(term_vec, set1)
    return term_vec


def calculate_co(terms, url):
    text_vec = text_to_vector(url_to_text(url))
    term_vec = term_vector(terms)
    return determine_cosine(term_vec, text_vec)



# with open('../pages/classification/accoustic_4.txt') as f1:
#     url = f1.readline()
#     url = url.split(' ')[1]
#     print(calculate_co(['logging', 'tracking'], url))


