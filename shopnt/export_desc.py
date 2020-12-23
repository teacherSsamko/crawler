import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

lst = os.walk('crawler/shopnt/texts')

for item in lst:
    root = item[0]
    with open(os.path.join(BASE_DIR, 'shopnt_description_201223.tsv'), 'w') as f:
        for t in item[2]:
            f.write(t.split(".")[0])
            f.write("\t")
            with open(os.path.join(root,t),'r') as txt:
                desc = txt.readlines()
                f.write(f'{"".join(desc)}\n')

    break
