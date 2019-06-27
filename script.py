import os
import sys
os.system('clear')

current_directory = os.getcwd()
sys.path.insert(0, '%s/config'%current_directory)
sys.path.insert(0, '%s/objects'%current_directory)

from env import *
import searcher
import scraper
import extractor
import storer
import input_structure_reader

systems = searcher.get_systems_from_file(env['systems_path'])
excluded_sources = searcher.get_excluded_sources_from_file(env['excluded_sources_path'])
google_search_terms = searcher.get_excluded_sources_from_file(env['search_terms_path'])
classes, classes_vec, searchterms = input_structure_reader.excel_to_classes_and_searchterms(env['terms_path'], classes_wordforms_expansion=True, classes_full_expansion=False, expansion_depth=1)

db = storer.create_database(env['sql_username'], env['sql_password'], 'c_uas')
# print('database created')
storer.add_tables(db)
# print('tables created')
# storer.insert_in_main_categories(db, 'test')
# storer.insert_in_systems(db, 5, 'system tester 2.0', 3)
# storer.insert_in_information(db, 1, 2, 'radar', 'aap noot mies', 'http://test.com', 'Er was eens, er waren eens, dat was het dus', 1)

for system in systems:
	manufacturer_id = storer.insert_in_manufacturers(db, system[0])
	if system[1] != '':
		# print('1', system[1], )
		system_id = storer.insert_in_systems(db, manufacturer_id, system[1])
	for google_search_term in google_search_terms:
		to_search = searcher.create_to_search(system, google_search_term)
		urls = searcher.google_term(to_search, excluded_sources, env['number_of_search_results'])
		for url in urls:
			text = scraper.get_text_from_url(url)
			if text:
				sentences = scraper.extract_sents(text)
				dictio = extractor.fillDict(searchterms, sentences, classes_vec, classes, env['nFreqWords'], env['surr_range'])
				for main_category in dictio:
					# print('main_category', main_category)
					main_category_id = storer.insert_in_main_categories(db, main_category)
					print('main_category_id', main_category_id)
					for category in dictio[main_category]:
						category_name = list(category.keys())[0]
						sub_category_id = storer.insert_in_sub_categories(db, category_name)
						keyterms = ' '.join(list(category.values())[0][0])
						context = list(category.values())[0][1]
						storer.insert_in_information(db, system_id, main_category_id, category_name, keyterms, url, context)
						print(url, 'stored')

