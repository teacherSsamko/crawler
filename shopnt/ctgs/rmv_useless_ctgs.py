import os
import csv

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

tsvfile = open(os.path.join(BASE_DIR, "final_ctg_copy.tsv"), newline='')
target = open(os.path.join(BASE_DIR, 'final_ctg_3.tsv'), 'w')

reader = csv.reader(tsvfile, delimiter='\t')
i = 1
total = 1178
reader.__next__()
for row in reader:
    ctgs = row[2].split(":")
    if ctgs[1] != ctgs[3] and ctgs[2] != ctgs[3]:
        target.write('\t'.join(row) + '\n')

tsvfile.close()
target.close()