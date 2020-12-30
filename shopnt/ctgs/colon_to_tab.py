import os
import re

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, "ctg_prods.tsv"), "r") as f:
    data = f.read()

data = re.sub("[:]", "\t", data)

with open(os.path.join(BASE_DIR, "ctg_prods_2.tsv"), "w") as f:
    f.write(data)