from tika import parser

raw = parser.from_file('CSD-Counter-Drone-Systems-Report.pdf')
file = open ('CSD-Counter-Drone-Systems-Report.txt', 'w')
content = raw['content']
for line in content:
	print('line', line)
# file.write(raw['content'])



