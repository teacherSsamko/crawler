import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, 'ctg_prods.txt'), 'r') as f:
    txt = f.readlines()

ctgs = set()

for r in txt:
    ctgs.add(r)

ctgs = list(ctgs)
ctgs.sort()
for ctg in ctgs:
    print(ctg, end='')
