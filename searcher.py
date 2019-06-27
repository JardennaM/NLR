from googlesearch import search 
import time

def get_systems_from_file(path):
	"""Functions takes the path to the systems.txt file as input
	and return a list of lists where each sublist contains the manufacturer
	and the name of the product. System.txt should contain the name of the
	manufacturer and the name of the product, seperated by a '|' symbol. 

	Parameters:
	path (string): Path to systems.txt

	Returns:
	list(systems): list of systems to examine later.

	"""

	file = open(path).readlines()

	systems = []
	for line in file:
		line = line.rstrip('\n').split('|')
		if len(line) == 1:
			systems.append([line[0], ''])
		else:
			systems.append(line)
	return systems

def get_excluded_sources_from_file(path):
	"""Functions takes the path to the excluded_sources.txt file as input
	and return a list of excluded sources. Excluded_sources.txt should contain
	an excluded source on each line.

	Parameters:
	path (string): Path to excluded_sources.txt

	Returns:
	list(excluded_sources): list of excluded source to remove from the
	searcher.

	"""
	return [item.rstrip('\n') for item in open(path).readlines()]

def get_searchterms_from_file(path):
	"""Functions takes the path to the searchterms.txt file as input
	and return a list of terms to search for. Searchterms.txt should contain
	a searchterm on each line.

	Parameters:
	path (string): Path to searchterms.txt

	Returns:
	list(searchterms): list of searchterms to search for each system.

	"""
	return [item.rstrip('\n') for item in open(path).readlines()]

def site_in_excluded(url, excluded):
	"""Returns true if the url originates from an excluded source, otherwise
	returns false.

	Parameters:
	url (string): path to website
	excluded (list): list of excluded sources

	Returns:
	boolean

	"""
	for site in excluded:
		if site in url:
			return False
	return True

def create_to_search(system, searchterm):
	if system[1] == '':
		return '%s %s'%(system[0], searchterm)
	else:
		return '%s %s %s'%(system[0], system[1], searchterm)

def google_term(to_search, excluded_sources, number_of_top_results=25):
	"""Takes a list of terms to search for using a search engine as input and 
	returns the urls of the top results as list. The list is also stored in a 
	urls.txt file. When recieving a server_overflow error, the program waits 15
	minutes before trying to 

	Parameters:
	to_search (list): list of terms to search for
	excluded_sources (list): list of sources to exclude from the search results
	@optional number_of_top_results (int): the number of results per 
											term to return.

	Returns:
	urls (list): a list of urls to retrieve the content from.

	"""

	urls = []

	try:
		for url in search(to_search, tld="co.in", num=number_of_top_results, stop=10, pause=1):
			if site_in_excluded(url, excluded_sources):
				urls.append(url)
	except:
		print('waiting')
		time.sleep(900)
	return urls
