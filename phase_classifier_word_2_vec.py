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
import numpy as np
import random

from string import punctuation
import operator
import gzip
import gensim
import logging
from extractor import *
import collections
import tensorflow as tf


# def maybe_download(filename, url, expected_bytes):
#     """Checks if the filename already has been downloaded from the url.  
#     If not, it uses the urllib.request Python module which retrieves a file from the given url argument, 
#     and downloads the file into the local code directory.
#     Checks the size of the file and makes sure it lines up with the expected file size, expected_bytes."""
#     if not os.path.exists(filename):
#         filename, _ = urllib.request.urlretrieve(url + filename, filename)
#     statinfo = os.stat(filename)
#     if statinfo.st_size == expected_bytes:
#         print('Found and verified', filename)
#     else:
#         print(statinfo.st_size)
#         raise Exception(
#             'Failed to verify ' + filename + '. Can you get to it with a browser?')
#     return filename


# with open('../pages/classification/camera (uv)_2.txt') as f1:
#     url = f1.readline()
#     url = url.split(' ')[1]
#     filename = maybe_download('../pages/classification/camera (uv)_2.txt', url, 31344016)


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
    
terms = getTerms()



# Read the data into a list of strings.
def read_data(filename):
    """Extract the first file as a list of words."""
    with open(filename) as f1:
        url = f1.readline()
        url = url.split(' ')[1]
        text = getTextFromUrl(url)
        sents = extractSents(text)
        sents_list = flatten(sents)
        return sents_list


def build_dataset(words, n_words):
    """Process raw inputs into a dataset."""
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(n_words - 1))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0  # dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reversed_dictionary


data_index = 0
# generate batch data
def generate_batch(data, batch_size, num_skips, skip_window):
    global data_index
    assert batch_size % num_skips == 0
    assert num_skips <= 2 * skip_window
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
    context = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    span = 2 * skip_window + 1  # [ skip_window input_word skip_window ]
    buffer = collections.deque(maxlen=span)
    for _ in range(span):
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
    for i in range(batch_size // num_skips):
        target = skip_window  # input word at the center of the buffer
        targets_to_avoid = [skip_window]
        for j in range(num_skips):
            while target in targets_to_avoid:
                target = random.randint(0, span - 1)
            targets_to_avoid.append(target)
            batch[i * num_skips + j] = buffer[skip_window]  # this is the input word
            context[i * num_skips + j, 0] = buffer[target]  # these are the context words
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
    # Backtrack a little bit to avoid skipping words in the end of a batch
    data_index = (data_index + len(data) - span) % len(data)
    return batch, context



# We pick a random validation set to sample nearest neighbors. Here we limit the
# validation samples to the words that have a low numeric ID, which by
# construction are also the most frequent.
valid_size = 16     # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)


batch_size = 128
embedding_size = 128  # Dimension of the embedding vector.
skip_window = 1       # How many words to consider left and right.
num_skips = 2         # How many times to reuse an input to generate a context.

train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
valid_dataset = tf.constant(valid_examples, dtype=tf.int32)


# Look up embeddings for inputs.
embeddings = tf.Variable(
    tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
embed = tf.nn.embedding_lookup(embeddings, train_inputs)


# Construct the variables for the softmax
weights = tf.Variable(tf.truncated_normal([vocabulary_size, embedding_size],
                          stddev=1.0 / math.sqrt(embedding_size)))
biases = tf.Variable(tf.zeros([vocabulary_size]))
hidden_out = tf.matmul(embed, tf.transpose(weights)) + biases

# convert train_context to a one-hot format
train_one_hot = tf.one_hot(train_context, vocabulary_size)
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hidden_out, 
    labels=train_one_hot))
# Construct the SGD optimizer using a learning rate of 1.0.
optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(cross_entropy)

# Compute the cosine similarity between minibatch examples and all embeddings.
norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
normalized_embeddings = embeddings / norm

valid_embeddings = tf.nn.embedding_lookup(
      normalized_embeddings, valid_dataset)

similarity = tf.matmul(
      valid_embeddings, normalized_embeddings, transpose_b=True)




words = read_data('../pages/classification/camera (uv)_2.txt')

terms = getTerms()

data, count, dictionary, reversed_dictionary = build_dataset(words, 1000)

batch, context = generate_batch(data, batch_size=5, num_skips=1, skip_window=2)

