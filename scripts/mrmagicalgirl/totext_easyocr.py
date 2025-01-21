import easyocr
import glob
import os
import shutil

dirs = []

for dirname in glob.glob("chapter*-*"):
    dirs.append(dirname)

reader = easyocr.Reader(['ko'])

for dir in dirs:
    try:
        if os.path.exists(dir + "/easyocr"):
            shutil.rmtree(dir + "/easyocr")
        os.mkdir(dir + "/easyocr")
    except OSError as e:
        print("Error deleting " + dir + "/easyocr: " + e.strerror)
        continue
    for filename in glob.glob(glob.escape(dir) + "/img/*.jpg"):
        result  = reader.readtext(filename, paragraph=True)
        fname = os.path.basename(filename)
        fout = open(dir + "/easyocr/" + fname[:-4] + "_kr.txt", 'w')
        for par in result:
            fout.write(par[1] + "\n")
    print("Done processing " + dir)
