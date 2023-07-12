import pandas as pd
from Bio import SeqIO

df = pd.read_csv("arvense/t-arvense.csv", header=0)

fasta_file = {}

with open("../T.arvense/Thlaspi-arvense-filtr.fna") as f:
	for record in SeqIO.parse(f, "fasta"):
		fasta_file[record.id] = str(record.seq)

#df2 = df[df['query_coverage'] >= 70]

coords = {}
sequences = []
for index, row in df.iterrows():
	coords[row['query_id']] = [row['found_id'], row['found_begin'], row['found_end']]

for element in coords:
	if coords[element][1] < coords[element][2]:
		coords[element].append('+')
		coords[element].append(fasta_file[coords[element][0]][coords[element][1]:coords[element][2]])
		sequences.append(fasta_file[coords[element][0]][coords[element][1]:coords[element][2]])
	else:
		coords[element].append('-')
		coords[element].append(fasta_file[coords[element][0]][coords[element][2]:coords[element][1]])
		sequences.append(fasta_file[coords[element][0]][coords[element][2]:coords[element][1]])

df3 = pd.DataFrame(coords)
df3 = df3.T
df3.columns = ["found_id", "found_begin", "found_end", "strand", "tRNA_gene"]
df3.index.name = "query_id"
df3.to_csv('t-arvense-genes-all.csv', index=True)

df['sequence'] = sequences
df.to_csv('arvense/t-arvense.csv', index=False)
