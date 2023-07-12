import pandas as pd
import numpy as np
import sys
from natsort import natsort_keygen

file = open(sys.argv[1], "r")

ids = []
begin = []
end = []
strand = []
aminoacid = []
anticodon = []

for line in file:
	if line.startswith('LT') or line.startswith('NC') or line.startswith('CM') or line.startswith('OU'):
		ids.append(f"{line.split()[0]}.trna{line.split()[1]}")
		if int(line.split()[2]) < int(line.split()[3]):
			begin.append(int(line.split()[2]))
			end.append(int(line.split()[3]))
			strand.append('+')
		else:
			begin.append(int(line.split()[3]))
			end.append(int(line.split()[2]))
			strand.append('-')
		aminoacid.append(line.split()[4])
		anticodon.append(line.split()[5])

d = {'id': ids, 'begin': begin, 'end': end, 'strand': strand, 'aminoacid': aminoacid, 'anticodon': anticodon}
df = pd.DataFrame(data=d)
df = df.sort_values(by=["strand", "id"], key=natsort_keygen())
df = df.reset_index(drop=True)

df_test_minus = df[df['strand'] == '-']
df_test_plus = df[df['strand'] == '+']
df_test_minus = df_test_minus.sort_values(by=['id', 'begin'], ascending=[False, True])

df_final = pd.concat([df_test_plus, df_test_minus])
df_final = df_final.reset_index(drop=True)

fn = sys.argv[2] + "-cut"
fn = fn.replace("/", "")
fn = fn.replace(".", "-")
fn = fn + ".csv"

df_final.to_csv(fn, index=True)

sub = []
sub_where = []

for i in range(len(df_final)-1):
    subtraction = df_final.loc[i+1, "begin"] - df_final.loc[i, "end"]
    if subtraction <= 1000 and subtraction > 0 and df_final.loc[i+1, "strand"] == df_final.loc[i, "strand"]:
	    sub.append(subtraction)
	    sub_where.append(i)
	    #sub_where.append(i+1)

filename = sys.argv[2] + "-clusters-ids"
filename = filename.replace("/", "")
filename = filename.replace(".", "-")
filename = filename + ".txt"

filename2 = sys.argv[2] + "-clusters"
filename2 = filename2.replace("/", "")
filename2 = filename2.replace(".", "-")
filename2 = filename2 + ".txt"

#tworzenie pliku z klastrami
f = open(filename, "a")
for i in range(0, len(sub_where)-1):
	f.write(f"{df_final.loc[sub_where[i], 'id']}\n")
	if sub_where[i+1] - sub_where[i] > 1:
		f.write(f"{df_final.loc[sub_where[i]+1, 'id']}\n")
f.write(f"{df_final.loc[sub_where[-1], 'id']}\n{df_final.loc[sub_where[-1]+1, 'id']}\n")
f.close()

f2 = open(filename2, "a")
for i in range(0, len(sub_where)-1):
	f2.write(df_final.loc[sub_where[i], "aminoacid"] + df_final.loc[sub_where[i], "anticodon"] + df_final.loc[sub_where[i], "strand"] + "::" + str(sub[i]) + "::")
	if sub_where[i+1] - sub_where[i] > 1:
		f2.write(df_final.loc[sub_where[i]+1, "aminoacid"] + df_final.loc[sub_where[i]+1, "anticodon"] + df_final.loc[sub_where[i]+1, "strand"] + "\n")
f2.write(df_final.loc[sub_where[-1], "aminoacid"] + df_final.loc[sub_where[-1], "anticodon"] + df_final.loc[sub_where[-1], "strand"] + "::" + str(sub[-1]) + "::" + df_final.loc[sub_where[-1]+1, "aminoacid"] + df_final.loc[sub_where[-1]+1, "anticodon"] + df_final.loc[sub_where[-1]+1, "strand"] + "\n")
f2.close()
