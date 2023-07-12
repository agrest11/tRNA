import sys

lengths = []
ids = {}

with open(sys.argv[1], "r") as f:
	for line in f:
		if "Length" in line:
			lengths.append(line.split()[3])
			id_trna = line.split(' ')[0]
			id_trna = id_trna.split('.')[0]
			if id_trna not in ids:
				ids[id_trna] = 1
			else:
				ids[id_trna] += 1

print(f"{sys.argv[1].split('/')[0]}\n{len(lengths)}\n{lengths}\n")

print(ids)
