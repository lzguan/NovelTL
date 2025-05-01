import json

with open('glossary_unprocessed.json', 'r') as f:
    glossary = json.load(f)

with open('glossary.txt', 'w') as f:
    cur = 0
    f.write('0: ')
    for k in glossary:
        if glossary[k] > cur:
            f.write("\n")
            cur = glossary[k]
            f.write(str(cur))
            f.write(": ")
        f.write(k)
        f.write(" ")