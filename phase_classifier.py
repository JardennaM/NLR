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
from copy import deepcopy
from extractor import *
from string import punctuation
import operator

phases = [['detection', 'detect', 'detector', 'detects', 'detecting'], 
['classification', 'identification', 'classify', 'reaction', 'idenitfy'],
['intent', 'intentionality', 'intention'], ['decision', 'decision support', 'decide'], 
['command', 'control', 'overall', 'main'], 
['intervention', 'intervene', 'interventions', 'neutralisation', 'neutralize', 'neutralise'], 
['forensics']]

classes = ['detection', 'classification', 'identification', 'intent', 'decision', 'command', 'control', 'intervention', 'neutralisation', 'forensics']


def determine_terms():
    """ 
        Creates a dictionary with all phases as key and as value their corresponding keywords stored in a list.
    """
    with open('keywords.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        keywords_dict = {}
        for row in csv_reader:
            keywords_dict[str(row[0])] = row[1:]
    return keywords_dict
    
terms = determine_terms()




def phase_classifier(url, terms):
    """ 
        Located keywords in the text of a webpage.
    """
    # Strip punctuation and make list of words in text
    text = strip_punctuation(url_to_text(url)).split(' ')
    # Get all unique searchterms.
    search_terms = list(set(flatten(list(terms.values()))))
    # Find indices of where there terms occur in the text.
    indices = find_index_of_term(search_terms, text)
    # Make dictionary with key the word and as value the surrounding keywords and their frequency.
    freq_sur_keyw = freq_sur_keywords(indices, search_terms, text)
    print(freq_sur_keyw)
    # Determine most_likely_phase for a word at a certain index
    most_likely_phase = most_likely_phases(indices, freq_sur_keyw, terms, text)
    return most_likely_phase

def strip_punctuation(text):
    return ''.join(word for word in text if word not in punctuation)

def find_index_of_term(search_terms, text):
    return [i for i, word in enumerate(text) for term in search_terms if word == term]

def freq_sur_keywords(indices, search_terms, text):
    """
        Make dictionary of the frequency of surrounding keywords with as key the center word and
        ans value a dictionary with the surrounding keywords and their frequency.
    """
    sur_word_freq = {}
    for i in indices:
        sur_text = surrounding_text(i, text, selection=700)
        sur_word_freq[text[i]] = freq_of_words(sur_text, search_terms)
    return sur_word_freq

def surrounding_text(index, text, selection):
    """
        Get surrounding text of a word given its index.
    """
    range_1 = index - selection
    range_2 = index + selection + 1
    if range_1 >= 0 and range_2 <= len(text):
        return text[range_1:range_2]
    elif range_1 >= 0:
        return text[range_1:len(text)]
    elif range_2 <= len(text):
        return text[0:range_2]
    else:
        return text[0:len(text)]

def freq_of_words(sur_text, search_terms):
    """
        Determine the frequency of a word and store in a dictionary.
    """
    overlapping_words = set(sur_text) & set(search_terms)
    word_freqs = Counter(sur_text)
    freq_dict = {}
    for word in overlapping_words:
        freq_dict[word] = word_freqs[word]
    return freq_dict



def most_likely_phases(indices, freq_sur_keyw, terms, text):
    likelyhoods_for_word = {}
    for i in indices:
        phase = determine_likelyhood(freq_sur_keyw, terms)
        max_phase = get_maximum(phase)
        likelyhoods_for_word[(text[i], i)] = max_phase
    return likelyhoods_for_word


def determine_likelyhood(freq_sur_keyw, terms):
    """
        Determines the most likely phase that a keyword found in the text belongs to based on the
        surrounding keywords found in the surroudning text.
    """
    score = {}
    for center_word in freq_sur_keyw:
        sur_key_list = [key for key in freq_sur_keyw[center_word]]
        for term in terms:
            phase_keys = terms[term]
            overlap = set(sur_key_list) & set(phase_keys)
            score[term] = phase_score(overlap, freq_sur_keyw, center_word, phase_keys)
    return score


def phase_score(overlap, freq_sur_keyw, center_word, phase_keys):
    """
        Determines the ratio of the amount of overlapping keywords and the keywords that 
        determines 
    """
    count = 0
    for word in overlap:
        count += freq_sur_keyw[center_word][word]
    return count / len(phase_keys)


def get_maximum(phase):
    maximum = max(phase)
    return [key for key in phase if phase[key] == phase[maximum]]




with open('../pages/classification/accoustic_2.txt') as f1:
    url = f1.readline()
    url = url.split(' ')[1]
    print(phase_classifier(url, determine_terms()))