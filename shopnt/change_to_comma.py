import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open('valid_related_prods.txt', 'r') as f:
    data = f.readlines()

new_data = []
for row in data:
    row = re.sub('[:]',',',row)
    new_data.append(row)

with open('valid_realted_prods_comma.csv', 'w') as csvfile:
    csvfile.write(''.join(new_data))