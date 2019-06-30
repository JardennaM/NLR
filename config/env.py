import sys

if sys.platform.startswith('win'):
	env = {
		'systems_path': r'config\systems.txt',
		'excluded_sources_path': r'config\excluded_sources.txt',
		'search_terms_path': r'config\search_terms.txt',
		'terms_path': r'config\terms.xlsx',
		'number_of_search_results': 25,
		'nFreqWords': 6,
		'surr_range': 1,
		'sql_username': 'root',
		'sql_password': ''
	}
else:
	env = {
		'systems_path': 'config/systems.txt',
		'excluded_sources_path': 'config/excluded_sources.txt',
		'search_terms_path': 'config/search_terms.txt',
		'terms_path': 'config/terms.xlsx',
		'number_of_search_results': 25,
		'nFreqWords': 6,
		'surr_range': 1,
		'sql_username': 'root',
		'sql_password': 'HoiHoi1!'
	}