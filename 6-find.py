import operator

all_clusters = []
org_clusters = []
names = []
clust = {}
clust_org = {}

with open("c.txt", "r") as f:
	for line in f:
		if not line == "\n":
			all_clusters.append(line.rstrip())
f.close()

list_set = set(all_clusters)
unique_clust = (list(list_set))

files = ["A.alpina/A-alpina-clusters-filtr.txt", "A.thaliana/A-thaliana-clusters-filtr.txt", "B.oleracea/B-oleracea-clusters-filtr.txt",
		"B.sinensis/B-sinensis-clusters-filtr.txt", "B.stricta/B-stricta-clusters-filtr.txt", "C.sativa/C-sativa-clusters-filtr.txt",
		"E.cheiranthoides/E-cheiranthoides-clusters-filtr.txt", "I.tinctoria/I-tinctoria-clusters-filtr.txt",
		"P.cornutum/P-cornutum-clusters-filtr.txt", "R.raphanistrum/R-raphanistrum-clusters-filtr.txt", "T.arvense/T-arvense-clusters-filtr.txt"]

for count, file in enumerate(files):
	with open(file, "r") as f2:
		for line in f2:
			if not line == "\n":
				org_clusters.append(line.rstrip())
	f2.close()

	org = []

	for clust1 in all_clusters:
		if clust1 in org_clusters:
			if clust1 not in clust:
				clust[clust1] = 1
			else:
				clust[clust1] += 1

			if clust1 in clust_org:
				# append the new number to the existing array at this slot
				if file.split("/")[0] not in clust_org[clust1]:
					clust_org[clust1].append(file.split("/")[0])
			else:
				# create a new array in this slot
				clust_org[clust1] = [file.split("/")[0]]

	org_clusters = []

d = dict(sorted(clust.items(), key=operator.itemgetter(1), reverse=True))

'''for key in clust_org:
	print(key, clust_org[key], "\n")'''

'''for key in d:
	if d[key] > 1:
		print(key, d[key])'''

for key in d:
	if key in clust_org and d[key] > 1:
		all_names = " ".join(clust_org[key])
		print(f"{key} {d[key]} {all_names}")

'''for key in d:
	if d[key] > 1:
		print(key, d[key])'''