organisms = ["A.alpina", "A.thaliana", "B.oleracea", "B.sinensis", "B.stricta", "C.sativa", "E.cheiranthoides", 
			"I.tinctoria", "P.cornutum", "R.raphanistrum", "T.arvense"]

org_clust = {}

def build_dict(elements):
	for element in elements:
		if element in organisms:
			if element not in org_clust:
				org_clust[element] = 1
			else:
				org_clust[element] += 1


with open('wyniki/zliczone_klastry_organizmy.txt') as f:
	for line in f:
		elements = line.split()
		build_dict(elements)
	org_clust = dict(sorted(org_clust.items()))
	for key in org_clust:
		print(f"{key} {org_clust[key]}")
