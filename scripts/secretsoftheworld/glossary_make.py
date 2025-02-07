from transformers import (
  AutoTokenizer,
  AutoModelForTokenClassification,
)
from transformers import pipeline
import glob
import os
import itertools
from enum import Enum
import json

tokenizer = AutoTokenizer.from_pretrained('tsmatz/xlm-roberta-ner-japanese')
model = AutoModelForTokenClassification.from_pretrained('tsmatz/xlm-roberta-ner-japanese')
nlp_ner = pipeline('ner', model=model, tokenizer=tokenizer)

indir = '../../../Database/secretsoftheworld/raw/'
glossary = {}

# ccc = ""
# with open(indir + "chapter_6.txt", 'r') as f:
#     for line in f:
#         ccc = ccc + line

# res = nlp_ner(ccc)
# print(res)

for i in itertools.count(start=1, step=1):
    print("chapter:", i)
    idx = 0
    chapter = ""
    ent = ""
    word = ""
    try:
        file = open(indir + "chapter_" + str(i) + ".txt", 'r')
    except FileNotFoundError:
        print(f"ERROR: File {i} not found")
        break
    with file:
        for line in file:
            chapter = chapter + line
    file.close()
    entities = nlp_ner(chapter)
    for e in entities:
        if e['word'] == '▁':
            continue
        if e['entity'] != ent or e['start'] > idx:
            if word:
                if not word in glossary:
                    glossary[word] = i
                word = ""
                
                
        if e['score'] > 0.9:
            idx = e['end']
            ent = e['entity']
            word = word + e['word']
        else:
            word = ""
    if word and not word in glossary:
        glossary[word] = i



with open('glossary_unprocessed.json', 'w') as file:
    json.dump(glossary, file)
    
        
# infile = '../../../Database/sheisnotawitch/raw/chapter_145.txt'
# text = ""

# with open(infile, 'r') as f:
#     for line in f:
#         text = text + line
# entities = nlp_ner(text)
# print(text)
# print(entities)
