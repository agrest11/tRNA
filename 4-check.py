import sys

f = open("wynik.txt", "r")

blocks = []

b = []
for line in f:
	if line != "\n":
		line = line.lstrip(" ")
		line = line.rstrip(" \n")
		b.append(line)
	else:
		blocks.append(b)
		b = []

blocks.remove(blocks[0])

new = []
n = []

for block in blocks:
	#print(block)
	for element in block:
		if element.startswith("Match"):
			if len(element.lstrip("Match: ")) >= 7:
				dif = len(block[0]) - len(block[1])
				if dif == -8 or dif == 8 or dif == -1 or dif == 1 or dif == -9 or dif == 9 or dif == 0 or dif == 11 or dif == -11 or dif == -3 or dif == 3 or dif == -7 or dif == 7:
					if float(block[2]) >= 0.6:
						#print(block, "\n")
						new.append([block[0], block[1]])
						n.append(block[3])

new2 = []

for bl in new:
	new2.append([bl[0].split("::"), bl[1].split("::")])

filename = sys.argv[1] + "-vs-" + sys.argv[2]
filename = filename.replace("/", "")
filename = filename.replace(".", "-")
filename = filename + ".txt"

end = open(filename, "a")
pair_number = 0
for pair in new2:
	number = 0
	j = 0
	i = 0
	if len(pair[0]) > len(pair[1]):
		while(j <= len(pair[1])):
			if pair[0][j] == pair[1][i]:
				j += 1
				i += 1
			else:
				number += 1
				j += 1
				if number > 1:
					break
			if j == len(pair[1]) and j == i:
				break
		if number <= 1:
			end.write(str(pair) + "\n" + str(n[pair_number]) + "\n")
			print(pair[0], pair[1])
			print(n[pair_number])
	elif len(pair[1]) > len(pair[0]):
		while(j <= len(pair[0])):
			if pair[0][i] == pair[1][j]:
				j += 1
				i += 1
			else:
				number += 1
				j += 1
				if number > 1:
					break
			if j == len(pair[0]) and j == i:
				break
		if number <= 1:
			end.write(str(pair) + "\n" + str(n[pair_number]) + "\n")
			print(pair[0], pair[1])
			print(n[pair_number])
	else:
		while(j < len(pair[0])):
			if pair[0][i] != pair[1][j]:
				number += 1
				if number > 1:
					break
			if j == len(pair[0]) and j == i:
				break
			j += 1
			i += 1
		if number <= 1:
			end.write(str(pair) + "\n" + str(n[pair_number]) + "\n")
			print(pair[0], pair[1])
			print(n[pair_number])
	pair_number += 1

end.close()