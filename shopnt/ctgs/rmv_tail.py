import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, 'ctg_codes.txt'), 'r') as f:
    txt = f.readlines()

new = []
for r in txt:
    tmp = r.split("|")
    if len(tmp) == 2:
        new.append('|'.join(tmp))
    else:
        new.append('|'.join(tmp[:2]) + '\n')

new = list(set(new))
new.sort()

with open(os.path.join(BASE_DIR, 'ctg_codes_2.txt'), 'w') as f:
    f.write(''.join(new))