import json
import os
import shutil
import glob

out = {}

rawsdir = "../../../Database/sheisnotawitch/raw/"

with open('glossary_edited.txt', 'r') as f, open('glossary_edited.json', 'w') as g:
    for line in f:
        bits = line.split()
        chap = bits[0]
        word = bits[1]
        with open(rawsdir + "chapter_" + chap + ".txt", 'r') as h:
            if not word in h.read():
                print("skipped " + word + " in chapter " + chap)
                continue
        if chap in out:
            out[chap].append(word)
        else:
            out[chap] = [word]
    json.dump(out, g)
print(out)