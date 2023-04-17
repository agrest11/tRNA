import sys
import pandas as pd

df_ref = pd.read_csv("A.thaliana/a-thaliana.csv", header=0)
ref_score = df_ref.loc[:,"score (bits)"]

indexes_ref = []
i = df_ref.index
for x in i:
	indexes_ref.append(x)

get_ref = []
for ids, index in zip(df_ref.loc[:,"id_sekwencji"], indexes_ref):
	if index == 0:
		get_ref.append(str(df_ref.loc[index,"score (bits)"]))
	else:
		if ids != df_ref.loc[index-1,"id_sekwencji"]:
			get_ref.append(str(df_ref.loc[index,"score (bits)"]))

df = pd.read_csv(sys.argv[1], header=0)

indexes = []
i = df.index
for x in i:
	indexes.append(x)

get = []
for ids, index in zip(df.loc[:,"id_sekwencji"], indexes):
	if index == 0:
		get.append(df.loc[index,:].to_list())
	else:
		if ids != df.loc[index-1,"id_sekwencji"]:
			get.append(df.loc[index,:].to_list())

per = []
df2 = pd.DataFrame(get, columns=df.columns)

def percentage(part, whole):
  return 100 * float(part)/float(whole)

for number, maks in zip(df2.loc[:,"score (bits)"], get_ref):
	number = float(number)
	per.append(str(percentage(number, maks)))

df_out = df2[['id_sekwencji', 'id_znalezione', 'Begin_1', 'Begin_2', 'End_1', 'End_2', 'długość', 'score (bits)', '%_identyczności']]
df_out["%_bitscore"] = per

filename = sys.argv[1].replace(".csv","")
filename = filename + "-filtr.csv"
df_out.to_csv(filename, index=False)