import pandas as pd

df = pd.read_csv('alpina.csv', header=0)

left = []
right = []
genes = []

for index, row in df.iterrows():
	#print(row['found_length'], row['gene_length'], row['query_begin'], row['query_end'], row['query_length'])
	left_flank = (101 - int(row['query_begin']))
	gene1 = 0
	gene2 = 0
	if left_flank < 0:
		gene1 = int(row['query_begin']) - 101
		left.append(0)
	else:
		left.append(left_flank)
	x = int(row['query_length']) - (100 + int(row['gene_length']))
	if x == 0:
		right.append(100)
	else:
		y = int(row['query_end']) - (100 + int(row['gene_length']))
		right_flank = round((y / x * 100), 2)
		if right_flank < 0:
			gene2 = (101 + int(row['gene_length'])) - int(row['query_end'])
			right.append(0)
		else:
			right.append(right_flank)
	if gene1 or gene2:
		gene = round((((int(row['gene_length']) - (gene1 + gene2)) / int(row['gene_length'])) * 100), 2)
		if gene > 0:
			genes.append(gene)
		else:
			genes.append(0)
	else:
		genes.append(100)

df['left_flank'] = left
df['right_flank'] = right
df['gene'] = genes

df.to_csv('a-alpina.csv', index=False)
