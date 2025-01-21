import glob
import os
import fileinput
import shutil

def convertChapToString(c):
    if c < 10:
        return "00" + str(c)
    elif 10 <= c and c < 100:
        return "0" + str(c)
    else:
        return str(c)

dirs = []
chap = 0
chaptext = ""
imginput = fileinput.input("imglist.txt")
imglist = []
imgindex = 0
for line in imginput:
    imglist.append(line[:-1])
imginput.close()
imglist[-1] = imglist[-1] + 'g'
for fname in imglist:
    imglist[imgindex] = fname[:-4] + '_kr.txt'
    imgindex = imgindex + 1
imgindex = 0
print(imglist)
ocr = "cloudvision"

for dirname in glob.glob("chapter*-*"):
    dirs.append(dirname)
try:
    if os.path.exists("./chapters_all"):
        shutil.rmtree("./chapters_all")
    os.mkdir("./chapters_all")
except OSError as e:
    print("Error deleting ./chapters_all: " + e.strerror)
    exit()

fout = open("./chapters_all/chapter_000.txt", "w")
fout2 = open("./chapter001-025/chapters/chapter_000.txt", "w")



for dir in dirs:
    try:
        if os.path.exists(dir + "/chapters"):
            shutil.rmtree(dir + "/chapters")
        os.mkdir(dir + "/chapters")
    except OSError as e:
        print("Error deleting " + dir + "/chapters: " + e.strerror)
        continue
    for filename in glob.glob(glob.escape(dir) + "/" + ocr + "/*_kr.txt"):
        fname = os.path.basename(filename)
        finput = fileinput.input(filename)
        if imgindex < len(imglist) and fname == imglist[imgindex]:
            fout.write("__IMG__" + filename + "\n")
            fout2.write("__IMG__" + filename + "\n")
            imgindex = imgindex + 1
            for line in finput:
                fout.write(line)
                fout2.write(line)
        else:
            chapcheck = ""
            firstLine = True
            for line in finput:
                if firstLine and line[0].isdigit():
                    chapcheck = line[0]
                    cnt = 1
                    while line[cnt].isdigit():
                        chapcheck = chapcheck + line[cnt]
                        cnt = cnt + 1
                    chapcheck = int(chapcheck)
                    if chapcheck == chap + 1:
                        chap = chap + 1
                        print(str(chap) + ": " + filename)
                        fout.close()
                        fout2.close()
                        fout = open("./chapters_all/chapter_" + convertChapToString(chap) + ".txt", "w")
                        fout2 = open("./" + dir + "/chapters/chapter_" + convertChapToString(chap) + ".txt", "w")
                fout.write(line)
                fout2.write(line)
            

        finput.close()
fout.close()
fout2.close()