import sys

clust = []
filtr = []
with open(sys.argv[1], "r") as data:
	while (line := data.readline().rstrip()):
		clust.append(line)

for i in range(0, len(clust)):
	j = 0
	string = ""
	string2 = ""
	for element in clust[i]:
		if element.isdigit():
			continue
		else:
			string += element
	if "-" in string:
		string = string.split()
		string = string[::-1]
		for l in string:
			string2 += l
		string2 = string2.replace("-", "")
		string2 += "\n"
	else:
		string2 = string.replace("+", "")
		string2 += "\n"
	filtr.append(string2.replace("::::", "::"))
	j += 1

filename = sys.argv[1] + "-cluster-filtr"
f = open(filename, "w")
for e in filtr:
	f.write(e + "\n")
	print(e)