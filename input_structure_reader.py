import pandas as pd
import numpy as np
from nltk.corpus import wordnet
import scraper
from scraper import flatten
from word_forms.word_forms import get_word_forms
import numpy as np

def get_all_word_forms(word):

	# get all word forms of a word in a list
	forms_dict = get_word_forms(word)

	return list(dict.fromkeys(flatten(forms_dict.values())))

def get_synonyms(word, depth):
	# get synset
	syns = wordnet.synsets(word)

	# extract synonyms of word from synset
	synonyms = []
	for syn in syns:
		synonyms.append([x.name() for i, x in enumerate(syn.lemmas()) if i < depth])

	# list the synonyms for the word
	synonyms = list(dict.fromkeys(flatten(synonyms)))

	return synonyms

def synset_classes(classes, depth):
	main_categories = []
	for main_cat in classes:
		synonyms = get_synonyms(main_cat, depth)
		all_forms = flatten([get_all_word_forms(x) for x in synonyms])
		all_forms = [x for x in all_forms if '_' not in x]
		main_categories.append(all_forms)


	return main_categories

def create_search_terms(methods, relevant_info):
	searchterms = []
	for i, class_methods in enumerate(methods):
		class_terms = []
		for method in class_methods:
			class_terms.append(method)
			for info_piece in relevant_info[i]:
				class_terms.append(method + info_piece)
		searchterms.append(class_terms)

	return searchterms

def reshape_input(input):

	for index, value in enumerate(input):
		split_list = [x.strip() for x in value.split(',')]
		split_list = [x.split(' ') for x in split_list]
		input[index] = split_list

	return input

def excel_to_classes_and_searchterms(file, classes_wordforms_expansion=False, classes_full_expansion=False, expansion_depth=1):
	# read excel
	df = pd.read_excel(file)

	# get classes/main categories
	classes = list(df.iloc[:,0].values)
	# shape methods list
	methods = reshape_input(list(df.iloc[:,1].values))
	# shape relevant info list
	relevant_info = reshape_input(list(df.iloc[:,2].values))


	searchterms = create_search_terms(methods, relevant_info)

	if classes_wordforms_expansion and classes_full_expansion:
		raise ValueError('ERROR: not possible to set both boolean values to True, set one to True or both to False')

	# EXPANSION
	if classes_wordforms_expansion:
		# expand classes with word forms
		classes_vec = [get_all_word_forms(class_) for class_ in classes]

	if classes_full_expansion:
		# we can also expand it with withforms AND synonyms at a specific depth
		classes_vec = synset_classes(classes, expansion_depth)

	if not classes_full_expansion and not classes_wordforms_expansion:
		classes_vec = [[x] for x in classes]
	

	return classes, classes_vec, searchterms
	


