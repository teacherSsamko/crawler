import os
import re

name = 'food'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, f'{name}.txt'), 'r') as f:
    txt = f.read()

with open(os.path.join(BASE_DIR, f'{name}_ctg.txt'), 'w') as f:
    f.write(re.sub('[:,]','\n',txt))
