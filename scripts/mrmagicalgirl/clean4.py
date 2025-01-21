import os
import glob




for file in glob.glob("chapters_all/*.txt"):
    out = ""
    with open(file, "r") as fin:
        for line in fin:
            if len(line) > 1:
                out = out + line
    with open(file, "w") as fout:
        fout.write(out)