from googlesearch import search 

# # # # # # # # # # # # # Create systems list # # # # # # # # # # # # # 

file = open('drone_systems.txt').readlines()

systems = []

for line in file:
	line = line.rstrip('\n').split('|')
	if len(line) == 1:
		systems.append([line[0], ''])
	else:
		systems.append(line)

# # # # # # # # # # # # # Create searchterms list # # # # # # # # # # # # # 

def checkExcluded(url, excluded):
	for site in excluded:
		if site in url:
			return False
	return True

urlFile = open('urls.txt', 'w')
excluded = [item.rstrip('\n') for item in open('excluded.txt').readlines()]

searchterms = ['specs', 'specifications', 'system']
toSearch = []

for system in systems:
	systemList = []
	if system[1] != '':
		for term in searchterms:
			systemList.append(system[0] + ' ' + system[1] + ' ' + term)
			systemList.append(system[1] + ' ' + term)
	[toSearch.append(item) for item in systemList]

count = 1
for term in toSearch:
	print(count, 'van de', len(toSearch))
	for url in search(term, tld="co.in", num=25, stop=10, pause=1):
		if checkExcluded(url, excluded):
			urlFile.write('%s\n'%url)
	count += 1
