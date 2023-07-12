import difflib
import sys
import os

clusters1 = open(sys.argv[1], "r")
clusters2 = open(sys.argv[2], "r")

base1 = []
base2 = []
base3 = []
base4 = []
filtr1 = []
filtr2 = []
id1 = []
id2 = []
clust1 = []
clust2 = []

clust = [clusters1, clusters2]
bases = [base1, base2]
bases2 = [base3, base4]
filters = [filtr1, filtr2]
ids = [id1, id2]

def get_first_base(cluster, base):
	for i in range(0, len(clust)):
		for line in cluster[i]:
			base[i].append(line.split())

def get_second_base(base, base_next):
	for i in range(0, len(bases)):
		for element in base[i]:
			for sign in element:
				base_next[i].append(sign)

def get_filtered(base, filtr, idss):
	for i in range(0, len(base)):
		j = 0
		for element in base[i]:
			string = ""
			string2 = ""
			for sign in element:
				if sign.isdigit():
					continue
				else:
					string += sign
			if "-" in string:
				idss[i].append(j)
				string = string.split()
				string = string[::-1]
				for l in string:
					string2 += l
				string2 = string2.replace("-", "")
				string2 += "\n"
			else:
				string2 = string.replace("+", "")
				string2 += "\n"
			filtr[i].append(string2.replace("::::", "::"))
			j += 1

def main():
	get_first_base(clust, bases)
	clusters1.close()
	clusters2.close()

	get_second_base(bases, bases2)

	get_filtered(bases2, filters, ids)

	#potrzebuję numery linii po przyrównaniu
	f = open("filtr1.txt", "a")
	for element in filtr1:
		f.write(element)
	f.close()
	f = open("filtr2.txt", "a")
	for element in filtr2:
		f.write(element)
	f.close()

	with open("filtr1.txt", "r") as file1, open("filtr2.txt", "r") as file2:
		while (line1 := file1.readline().rstrip()):
			clust1.append(line1)
		while (line2 := file2.readline().rstrip()):
			clust2.append(line2)

	file1.close()
	file2.close()

	for i in range(0, len(clust1)):
		for j in range(0, len(clust2)):
			sm = difflib.SequenceMatcher(None, clust1[i], clust2[j])
			rat = difflib.SequenceMatcher(None, clust1[i], clust2[j]).ratio()
			print("\n", clust1[i], "\n", clust2[j], "\n", rat)	#print("\n", i, clust1[i], "\n", j, clust2[j], "\n", rat)
			print(i+1, j+1)
			# Iterate over the differences and print them
			for tag, i1, i2, j1, j2 in sm.get_opcodes():
				if tag == "insert":
					print(f"Insertion: {clust2[j][j1:j2]}")
				elif tag == "delete":
					print(f"Deletion: {clust1[i][i1:i2]}")
				elif tag == "replace":
					print(f"Replacement: {clust1[i][i1:i2]} => {clust2[j][j1:j2]}")
				else:
					print(f"Match: {clust1[i][i1:i2]}")

if __name__ == "__main__":
	main()