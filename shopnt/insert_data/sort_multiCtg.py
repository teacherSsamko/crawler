import os
import csv


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, "multiCtg_ids.txt"), newline='') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    max = 0
    for row in reader:
        if int(row[0]) > max:
            max = int(row[0])

    print(max)