import os.path
import sys

chap = 1
rawdir = '../../../Database/secretsoftheworld/raw/'

while os.path.isfile(rawdir + "chapter_" + str(chap) + ".txt"):
    with open (rawdir + "chapter_" + str(chap) + ".txt", 'r') as f:
        s = f.read()
        if sys.argv[1] in s:
            print(chap)
    chap = chap + 1
