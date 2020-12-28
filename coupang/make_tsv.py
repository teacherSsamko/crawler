import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR,'catgs.txt'), 'r') as f:
    data = f.readlines()

new_data = []
for row in data:
    row = re.sub('[$]','\t',row)
    new_data.append(row)

with open('coupang/coupang_categories.tsv', 'w') as csvfile:
    csvfile.write(''.join(new_data))