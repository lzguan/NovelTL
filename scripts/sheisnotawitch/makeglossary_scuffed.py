from transformers import (
  BertTokenizerFast,
  AutoModelForTokenClassification,
)
from transformers import pipeline
import glob
import os
import itertools
from enum import Enum
import json

tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
model = AutoModelForTokenClassification.from_pretrained('ckiplab/bert-base-chinese-ner')
nlp_ner = pipeline('ner', model=model, tokenizer=tokenizer)

indir = '../../../Database/sheisnotawitch/raw/'
glossary = {}

tags = [
    "-EVENT", "-FAC", "-GPE", "-LANGUAGE", "-LAW", "-LOC",
    "-NORP", "-ORG", "-PERSON", "-PRODUCT", "-WORK_OF_ART"
]

class State(Enum):
    wait = 0
    processing = 1

curstate = State.wait


for i in itertools.count(start=0, step=1):
    print("chapter:", i)
    ent = ""
    tail = ""
    head = ""
    type = ""
    chapter = ""
    try:
        file = open(indir + "chapter_" + str(i) + ".txt", 'r')
    except FileNotFoundError:
        break
    with file:
        for line in file:
            chapter = chapter + line
    entities = nlp_ner(chapter)
    for e in entities:
        if curstate == State.wait:
            ent = ""
            head = e['entity'][0]
            tail = e['entity'][1:]
            if not tail in tags:
                continue
            if head == "S" and not e['word'] in glossary:
                glossary['word'] = i
            elif head == "B":
                curstate = State.processing
                ent = ent + e['word']
                type = tail
            else:
                ent = ""
                curstate = State.wait
        elif curstate == State.processing:
            head = e['entity'][0]
            tail = e['entity'][1:]
            if tail != type:
                ent = ""
                curstate = State.wait
            if head == "B" or head == "S":
                ent = ""
                curstate = State.wait
            if head == "I":
                ent = ent + e['word']
            elif head == "E":
                ent = ent + e['word']
                if not ent in glossary:
                    glossary[ent] = i
                curstate = State.wait
            else:
                ent = ""
                curstate = State.wait
    if curstate == State.processing:
        if not ent in glossary:
            glossary[ent] = i
        curstate = State.wait

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
