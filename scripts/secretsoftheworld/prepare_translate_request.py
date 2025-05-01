import json
import os
import shutil
import glob

dirout = "./chapters_all_jsonl"

glossaryfile = 'glossary_translated.csv'
rawdir = '../../../Database/secretsoftheworld/raw/'
bindir = 'bin/'

glossary = {}

with open(glossaryfile, 'r') as gf:
    for line in gf:
        ln = line.strip('\n').split(",")
        glossary[ln[0]] = ln[1]


gcur = ""
request_num = 1
newchap = True
isImg = False
sysprompt = "You are a translating a Japanese webnovel called \\\"世界の秘密を教えてあげる\\\" to english. It is a romance fantasy novel. Do not add any additional text. A glossary of terms appearing in this chapter is listed below (if there are any) in the format \\\"Japanese name\\\": \\\"English name\\\":\\n"
pre = "\"Translate the following chapter into English. For terms in the glossary, use the glossary to translate them. Mantain the original style of the author when appropriate.\\n"
fout = open("translate_request.jsonl", "w")
chapdata = {}
for chapnum in range(1, 97):
    chapdata[chapnum] = []
    file = rawdir + "chapter_" + str(chapnum) + ".txt"
    charbuf = ""
    print("Chapter " + str(chapnum))
    gcur = ""
    with open(file, 'r') as fin:
        txt = fin.read()
        for key in glossary:
            if key in txt:
                gcur = gcur + key + ": " + glossary[key].replace("\"","\\\"") + "\\n"
    with open(file, "r") as fin:
        for line in fin:
            charbuf = charbuf + line.strip().replace("\"", "\\\"") + "\\n"
            if len(charbuf) > 3500:
                b1 = "{\"role\": \"system\", \"content\": \"" + sysprompt + "\"}"
                b2 = "{\"role\": \"user\", \"content\": " + pre + charbuf + "\"}"
                body = "{\"model\": \"gpt-4o\", \"messages\": [" + b1 + ", " + b2 + "]}"
                requestr = "{\"custom_id\": \"request_" + str(request_num) + "\", \"method\": \"POST\", \"url\": \"/v1/chat/completions\", \"body\": " + body + "}"
                fout.write(requestr + "\n")
                charbuf = ""
                chapdata[chapnum].append("request_" + str(request_num))
                request_num = request_num + 1
        if len(charbuf.strip()) > 0:
            b1 = "{\"role\": \"system\", \"content\": \"" + sysprompt + gcur + "\"}"
            b2 = "{\"role\": \"user\", \"content\": " + pre + charbuf + "\"}"
            body = "{\"model\": \"gpt-4o\", \"messages\": [" + b1 + ", " + b2 + "]}"
            requestr = "{\"custom_id\": \"request_" + str(request_num) + "\", \"method\": \"POST\", \"url\": \"/v1/chat/completions\", \"body\": " + body + "}"
            fout.write(requestr + "\n")
            chapdata[chapnum].append("request_" + str(request_num))
            request_num = request_num + 1
            charbuf = ""

fsupp = open("chapter_data.json", 'w')
json.dump(chapdata, fsupp)
fout.close()