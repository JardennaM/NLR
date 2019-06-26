import configurator
import searcher
import scraper
import extractor
import bottom_up
import re
from paths import *
import os

os.system('clear')

systems = searcher.get_systems_from_file(paths['systems'])
excluded_sources = searcher.get_excluded_sources_from_file(paths['excluded_sources'])
searchterms = searcher.get_excluded_sources_from_file(paths['searchterms'])
# synonyms for phases
phases = [['detection', 'detect', 'detector', 'detects', 'detecting', 'recognize'], 
['classification', 'identification', 'classify', 'reaction', 'idenitfy'],
['intent', 'intentionality', 'intention'], 
['decision', 'decision support', 'decide'], 
['command', 'control', 'overall', 'main'], 
['intervention', 'intervene', 'interventions', 'neutralisation', 'neutralize', 'neutralise'], 
['forensics', 'forensic']]

# the actual classes (phases)
classes = ['detection', 'classification', 'intent', 'decision', 'command/control', 'intervention/neutralisation', 'forensics']

    
# the keyword terms to search for in the text
searchterms = ['acoustic', 'frequency', 'frequencies', 'radar', 'infrared camera', 'uv camera', 'multi-spectral camera', 'LIDAR', 'jamming', 'jammer'
'gui', 'method', 'integration', 'architecture', 'capture', 'kinetic', 'datalink jamming', 'gps jamming', 'laser', 'microwave']


# # GET NEEDED INFO
nFreqWords = 5
nSelection = 20

for system in systems:
	for searchterm in searchterms:
		to_search = system.create_to_search(searchterm)
		urls = searcher.google_term(to_search, excluded_sources, 10)
		for url in urls:
			try:
				text = scraper.getTextFromUrl(url)
				sentences = scraper.extractSents(text)
				worded_text = scraper.flatten(sentences)
				dictio = bottom_up.fillDict(searchterms, sentences, worded_text, phases, classes, nFreqWords, nSelection)
				print('url', url, '\n')
				for phase in dictio:
					print(phase, dictio[phase], '\n\n')
			except:
				print('noop')