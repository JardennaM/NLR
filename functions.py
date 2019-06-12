def getTerms(termsLink):
	"""Extract the terms from in the specified file and store them
	in a dictionary where the key is the phase"""
	terms = {}

	df = pd.read_excel('%s'%self.termsLink, index_row=0)
	columnNames = df.columns 
	for name in columnNames:
		terms[name] = []
		for item in df[name]:
			if type(item) != float:
				terms[name].append(item)
	return terms
