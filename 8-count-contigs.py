import sys

lengths = []

with open(sys.argv[1], "r") as f:
	for line in f:
		if "Length" in line:
			lengths.append(line.split()[3])

print(f"{sys.argv[1].split('/')[0]}\n{len(lengths)}\n{lengths}\n")