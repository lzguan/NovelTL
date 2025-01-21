import json
import glob
import os
import shutil

bindir = "bin"
rawdir = "chapters_all_jsonl"
outdir = "chapters_all_en"

imglist = []
with open("imglist.txt", "r") as fimglist:
    for line in fimglist:
        imglist.append(line.strip())
imglist = imglist[1:]

chapcnt = 0
reqcnt = 0
img_ptr = 0

try:
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
except OSError as e:
    print("Error deleting " + outdir + ": " + e.strerror)
    exit()

with open(bindir + "/chapters_translated.jsonl", "r") as frequests:
    for chap in glob.glob(glob.escape(rawdir) + "/*.jsonl"):
        with open(chap, "r") as fchap, open(outdir + "/chapter_" + str(chapcnt) + ".txt", "w") as wchap:
            for line in fchap:
                if len(line) > 0:
                    temp = json.loads(line)
                    id = temp['custom_id']
                    print("Processing request " + id)
                    id_num = int(id[8:])
                    while id_num > reqcnt + 1:
                        print("Image at chapter " + str(chapcnt))
                        print("id_num: " + str(id_num))
                        print("reqcnt:" + str(reqcnt))
                        print("img_ptr:" + str(img_ptr))
                        wchap.write("__IMG__" + imglist[img_ptr] + "\n")
                        reqcnt = reqcnt + 1
                        img_ptr = img_ptr + 1
                    curline = frequests.readline()
                    curjson = json.loads(curline)
                    text = curjson['response']['body']['choices'][0]['message']['content']
                    wchap.write(text + "\n")
                    reqcnt = reqcnt + 1
        chapcnt = chapcnt + 1