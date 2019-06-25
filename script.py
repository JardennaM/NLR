import configurator
import searcher
import scraper
import extractor
from paths import *

systems = searcher.get_systems_from_file(paths['systems'])
excluded_sources = searcher.get_excluded_sources_from_file(paths['excluded_sources'])
searchterms = searcher.get_excluded_sources_from_file(paths['searchterms'])
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

nFreqWords = 6
nSelection = 20

for system in systems:
	for searchterm in searchterms:
		to_search = system.create_to_search(searchterm)
		urls = searcher.google_term(to_search, excluded_sources, 10)
		for url in urls:
			if 'aaronia' not in url:
				print('url', url)
				try:
					text = scraper.get_text_from_url(url)
					sentences = scraper.extractSents(text)
					cleaned_sentences = scraper.extract_cleaned_sentences(text)
					dictio = fillDict(searchterms, sentences, cleaned_sentences, phases, classes, nFreqWords, nSelection)
					print('yes')
				except:
					print('noop')