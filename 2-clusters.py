import pandas as pd
import numpy as np
import sys

file = open(sys.argv[1], "r")

ids = []
begin = []
end = []
strand = []
aminoacid = []
anticodon = []

for line in file:
	if line.startswith('LT') or line.startswith('NC') or line.startswith('NW') or line.startswith('CM') or line.startswith('JA') or line.startswith('VW') or line.startswith('VH') or line.startswith('OU') or line.startswith('CA'):
		ids.append(line.split()[0])
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
df = df.sort_values(by=["id", "begin"])
df = df.reset_index(drop=True)

#df.to_csv("cut.csv", index=True)

sub = []
sub_where = []

for i in range(len(df)-1):
    subtraction = df.loc[i+1, "begin"] - df.loc[i, "end"]
    if subtraction <= 1000 and subtraction > 0 and df.loc[i+1, "strand"] == df.loc[i, "strand"]:
	    sub.append(subtraction)
	    sub_where.append(i)
	    #sub_where.append(i+1)

filename = sys.argv[2] + "-clusters"
filename = filename.replace("/", "")
filename = filename.replace(".", "-")
filename = filename + ".txt"

#tworzenie pliku z klastrami
f = open(filename, "a")
for i in range(0, len(sub_where)-1):
	f.write(df.loc[sub_where[i], "aminoacid"] + df.loc[sub_where[i], "anticodon"] + df.loc[sub_where[i], "strand"] + "::" + str(sub[i]) + "::")
	if sub_where[i+1] - sub_where[i] > 1:
		f.write(df.loc[sub_where[i]+1, "aminoacid"] + df.loc[sub_where[i]+1, "anticodon"] + df.loc[sub_where[i]+1, "strand"] + "\n")
f.write(df.loc[sub_where[-1], "aminoacid"] + df.loc[sub_where[-1], "anticodon"] + df.loc[sub_where[-1], "strand"] + "::" + str(sub[-1]) + "::" + df.loc[sub_where[-1]+1, "aminoacid"] + df.loc[sub_where[-1]+1, "anticodon"] + df.loc[sub_where[-1]+1, "strand"] + "\n")
f.close