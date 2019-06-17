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

from string import punctuation
import operator
import gzip
import gensim
import logging




logging.basicConfig(format=’%(asctime)s : %(levelname)s : %(message)s’, level=logging.INFO)


 
with gzip.open (input_file, 'rb') as f:
        for i,line in enumerate (f):
            print(line)
            break
 
def read_input(input_file):
    """This method reads the input file which is in gzip format"""
 
    logging.info("reading file {0}...this may take a while".format(input_file))
    with gzip.open(input_file, 'rb') as f:
        for i, line in enumerate(f):
 
            if (i % 10000 == 0):
                logging.info("read {0} reviews".format(i))
            # do some pre-processing like tokenzing and lowercasing and return list of words for each review
            # text
            yield gensim.utils.simple_preprocess(line)


# build vocabulary and train model
    model = gensim.models.Word2Vec(
        documents,
        size=150,
        window=10,
        min_count=2,
        workers=10,
        iter=10)