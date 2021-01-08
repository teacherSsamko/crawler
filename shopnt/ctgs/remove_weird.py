import os
import csv


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

doc = ''

with open(os.path.join(BASE_DIR, "ctg_prods_2.tsv"), newline='') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    i = 1
    total = 297765
    for row in reader:
        if row[1] != row[3] and row[2] != row[3]:
            doc += '\t'.join(row) + '\n'

with open(os.path.join(BASE_DIR, 'ctg_prods_tmp.tsv'), 'w') as f:
    f.write(doc)