from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx


def read_article(file_name):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []
    print(article)
   	for sentence in article:
		print(sentence)
	 	sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
	 	sentences.pop() 
    
    return sentences

print(read_article('pages/classification/accoustic_5.txt'))