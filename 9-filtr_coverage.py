import sys
import pandas as pd

# read Arabidopsis thaliana csv - blast output
df_ref = pd.read_csv("thaliana/blast-thaliana.csv", header=0)

# read another organism csv - blast output
df = pd.read_csv('arvense/blast-arvense.csv', header=0)

# get only rows with max 'score_percent' value for a given id and write them into dataframe
ref_score_percent_idx = df_ref.groupby(['query_id'])['score'].transform(max) == df_ref['score']
df_ref_score_percent = df_ref[ref_score_percent_idx]
# additional filter if max 'score_percent' is multipled
ref_score_percent_idx2 = df_ref_score_percent.groupby(['query_id'])['identities'].transform(max) == df_ref_score_percent['identities']
df_ref_score_percent2 = df_ref_score_percent[ref_score_percent_idx2]
df_ref_score_percent2 = df_ref_score_percent2.drop_duplicates(subset=['query_id'])

percent = []
for index, row in df.iterrows():
	for index2, row2 in df_ref_score_percent2.iterrows():
		if row['query_id'] == row2['query_id']:
			score_percent = round((row['score'] / row2['score'] * 100), 2)
			percent.append(score_percent)
df['score_percent'] = percent

# get only rows with max 'score_percent' value for a given id and write them into dataframe
score_percent_idx = df.groupby(['query_id'])['score_percent'].transform(max) == df['score_percent']
df_score_percent = df[score_percent_idx]
# additional filter if max 'score_percent' is multipled
score_percent_idx2 = df_score_percent.groupby(['query_id'])['identities'].transform(max) == df_score_percent['identities']
df_score_percent2 = df_score_percent[score_percent_idx2]

# check which ids are in both organisms - based on reference and based on another organism
df_ids_ref = df_ref_score_percent2.assign(InDf=df_ref_score_percent2['query_id'].isin(df_score_percent2['query_id']).astype(int))
df_ids = df_score_percent2.assign(InDf=df_score_percent2['query_id'].isin(df_ref_score_percent2['query_id']).astype(int))

# write to dataframe only these rows which ids are in reference organism
df_ref_selected_ids = df_ids_ref[df_ids_ref['InDf'] == 1]
# remove duplicated rows - these are our repeated genes!
df_ref_selected_ids2 = df_ref_selected_ids.drop_duplicates(subset=['query_id'])
df_ref_selected_ids2 = df_ref_selected_ids2.reset_index()

# write to dataframe only these rows which ids are in another organism
df_selected_ids = df_ids[df_ids['InDf'] == 1]
# remove duplicated rows - these are our repeated genes!
df_selected_ids2 = df_selected_ids.drop_duplicates(subset=['query_id'])
df_selected_ids2 = df_selected_ids2.reset_index()

# write duplicates to dataframe - reference
duplicated_ref = df_ref_selected_ids.assign(Duplicated=df_ref_selected_ids.duplicated(['query_id']).astype(int))
duplicated_ref2 = duplicated_ref[duplicated_ref['Duplicated'] == 1]
duplicated_ref2 = duplicated_ref2.reset_index()

#duplicated_ref2.to_csv('a-thaliana-duplicated.csv', index=False)

# write duplicates to dataframe - another organism
duplicated = df_selected_ids.assign(Duplicated=df_selected_ids.duplicated(['query_id']).astype(int))
duplicated2 = duplicated[duplicated['Duplicated'] == 1]
duplicated2 = duplicated2.reset_index()

duplicated3 = duplicated2.copy()
# duplicated3 = duplicated3.drop(columns=['InDf', 'index', 'mismatch', 'gaps', 'expected', 'Duplicated'])
duplicated3 = duplicated3.drop(columns=['InDf', 'index', 'Duplicated'])
duplicated3 = duplicated3.reset_index()
duplicated3.to_csv('t-arvense-duplicated.csv', index=False)



final = df_selected_ids2.copy()
# final = final.drop(columns=['InDf', 'index', 'mismatch', 'gaps', 'expected'])
final = final.drop(columns=['InDf', 'index'])
final = final.reset_index()

'''final2 = final[final['score_percent'] >= 60]
print(final2)'''


gene_ids = {}

with open('genes.txt', 'r') as f:
	for line in f:
		if line.startswith('>'):
			line = line.strip().lstrip('>').split()
			gene_length = int(line[3]) - int(line[2])
			if int(line[2]) > int(line[3]):
				gene_length *= -1
			gene_ids[line[0]] = gene_length

gene_length2 = []
for gene in gene_ids:
	if gene in final['query_id'].unique():
		gene_length2.append(gene_ids[gene])


'''final_ref = df_ref_selected_ids2.copy()
# final_ref = final_ref.drop(columns=['InDf', 'index', 'mismatch', 'gaps', 'expected'])
final_ref = final_ref.drop(columns=['InDf', 'index'])
final_ref = final_ref.reset_index()
final_ref['score_percent'] = '100'

gene_length_ref = []
for gene in gene_ids:
	if gene in final_ref['query_id'].unique():
		gene_length_ref.append(gene_ids[gene])

final_ref['gene_length'] = gene_length_ref
final_ref['query_length'] = df_ref_selected_ids2['found_length']'''


final['gene_length'] = gene_length2

final['query_length'] = df_ref_selected_ids2['found_length']

final.to_csv('arvense.csv', index=False)
# final_ref.to_csv('thaliana.csv', index=False)
