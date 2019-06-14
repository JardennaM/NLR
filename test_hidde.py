file = open('drone_systems.txt').readlines()

systems = []

for line in file:
	line = line.rstrip('\n').split('|')
	if len(line) == 1:
		systems.append([line[0], ''])
	else:
		systems.append(line)

print(systems)