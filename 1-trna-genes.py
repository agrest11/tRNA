from Bio import SeqIO as seqio
from Bio import SeqFeature as feat
from Bio.SeqFeature import FeatureLocation as featloc
from Bio.Seq import Seq
import re
import sys

sequences_ids = []
sequences_from_fasta = []
sequences_descriptions = []
for seq_file in seqio.parse(sys.argv[1], "fasta"):
    sequences_ids.append(seq_file.id)
    sequences_from_fasta.append(seq_file.seq)
    sequences_descriptions.append(seq_file.description)

coords = {}
n = open(sys.argv[2], "r")
new_ids = []
sequences_from_ss = []
for line in n:
    for ids in sequences_ids:
        if line.startswith(ids):
            x = re.findall(r'\w*_?\d*.\d.trna\d*', line)
            new_ids.append(x[0])
    for ids in new_ids:
        if line.startswith(ids + ' '):
            x = re.findall(r'\d*-\d*', line)
            y = re.findall(r'\d*', x[0])
            coords[ids] = [int(y[0]), int(y[2])]
    if line.startswith("Seq: "):
        sequences_from_ss.append(line.strip("Seq: ").strip("\n"))

i = 0
for ids in coords:
    first = coords[ids][0]
    second = coords[ids][1]
    coords[ids] = [first, second, sequences_from_ss[i]]
    i += 1

strand = []


def which_strand(seq_coord1, seq_coord2, sequence):
    if seq_coord2 > seq_coord1:
        strand.append('+')
    if seq_coord1 > seq_coord2:
        sequence = Seq(sequence)
        sequence = sequence.reverse_complement()
        strand.append('-')


starts = []
ends = []


def get_with_flanks(fragment_id, start, end):
    for i in range(0, len(sequences_from_fasta)):
        if sequences_ids[i] in fragment_id:
            with_flanks = ""
            if start > end:
                temp = start
                start = end
                end = temp
            minus = 101
            plus = 100
            if start < 100:
                minus = 100 - (100 - start)
            if end > len(sequences_from_fasta[i]) - 100:
                plus = len(sequences_from_fasta[i]) - end
            for j in range(start - minus, end + plus):
                with_flanks += "".join(sequences_from_fasta[i][j])
            starts.append(start - minus)
            ends.append(end + plus)
    return with_flanks


if __name__ == '__main__':
    flanks = []
    for key in coords:
        which_strand(coords[key][0], coords[key][1], coords[key][2])
    i = 0
    for ids in coords:
        first = coords[ids][0]
        second = coords[ids][1]
        third = coords[ids][2]
        coords[ids] = [first, second, third, strand[i]]
        i += 1
    for key in coords:
        flanks.append(get_with_flanks(key, coords[key][0], coords[key][1]))

    '''filename = sys.argv[3] + "-flanks"
    filename = filename.replace("/", "")
    filename = filename.replace(".", "-")
    filename = filename + ".fa"
    new_file = open(filename, "a")
    i = 0
    for flank in flanks:
        new_file.write('>{} | {} {} | {}'.format(new_ids[i], starts[i], ends[i], strand[i]))
        new_file.write("\n" + flank + "\n")
        i += 1
    new_file.close()'''

    with open('genes.txt', 'w') as f:
        for coord in coords:
            f.write('>{} | {} {}'.format(coord, coords[coord][0], coords[coord][1]))
            f.write("\n" + coords[coord][2] + "\n")
