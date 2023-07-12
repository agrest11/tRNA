import sys

ids_from_clusters = []
single = []
double = []
sequences = []
db_sequences = []

with open(sys.argv[1], "r") as f, open(sys.argv[2], "r") as f2:
	for line in f:
		ids_from_clusters.append(line.rstrip())
	for line2 in f2:
		if line2.startswith(">"):
			if line2.lstrip(">").split()[0] not in ids_from_clusters:
				single.append(line2.lstrip(">").split()[0])
				sequences.append(f2.readline().rstrip())
			else:
				double.append(line2.lstrip(">").split()[0])
				db_sequences.append(f2.readline().rstrip())

filename = sys.argv[1].replace("-clusters-ids", "-not-clusters")
filename2 = sys.argv[1].replace("-clusters-ids", "-in-clusters")

with open(filename, "w") as f3:
	for num, ids in enumerate(single):
		f3.write(">{}\n{}\n".format(ids, sequences[num]))

with open(filename2, "w") as f4:
	for num, ids in enumerate(double):
		f4.write(">{}\n{}\n".format(ids, db_sequences[num]))