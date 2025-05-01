import json
import pandas as pd

bin = "bin/"

chap = 0
gloss = {}

with open(bin + "glossary_translated.jsonl", 'r') as f, open("glossary.txt", 'r') as g:
    while True:
        tline = f.readline().strip("\n")
        if not tline:
            break
        gline = g.readline()
        tline = json.loads(tline)
        tline = tline['response']['body']['choices'][0]['message']['content'].split("\n")

        gline = gline.split()
        chap = gline[0][:-1]
        gline = gline[1:]
        for i in range(len(gline)):
            if i < len(tline):
                gloss[gline[i]] = tline[i]
            else:
                gloss[gline[i]] = "ERROR"
pd.DataFrame.from_dict(data=gloss, orient='index').to_csv('glossary_translated.csv', header=False)