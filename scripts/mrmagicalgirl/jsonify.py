import json
import os
import shutil
import glob

dirin = "./chapters_all"
dirout = "./chapters_all_jsonl"

try:
    if os.path.exists(dirout):
        shutil.rmtree(dirout)
    os.mkdir(dirout)
except OSError as e:
    print("Error deleting " + dirout)
    exit()

request_num = 0
newchap = True
isImg = False
sysprompt = "You are a translating a Korean webnovel called \\\"Mr. Magical Girl\\\" to english. It is a supernatural fantasy novel set in an alternate modern day Korea. In this world, portals to the otherworld spawn monsters to invade earth and certain people are selected as \\\"Awakeners\\\" (or Heroes) to fight the monsters. Do not add any additional text."
pre = "\"Translate the following Korean text into English while maintaining the original tone, style, and nuance. Do not simplify or summarize; keep names, cultural references, and terminology intact. If there are phrases or concepts without direct English equivalents, provide the closest natural translation.\\n"
for file in glob.glob(glob.escape(dirin) + "/*"):
    charbuf = ""
    print(dirout + "/" + os.path.basename(file)[:-4] + ".jsonl")
    with open(file, "r") as fin:
        with open(dirout + "/" + os.path.basename(file)[:-4] + ".jsonl", "w") as fout:
            for line in fin:
                if len(line) >= 7 and line[0:7] == "__IMG__":
                    if len(charbuf) > 0:
                        b1 = "{\"role\": \"system\", \"content\": \"" + sysprompt + "\"}"
                        b2 = "{\"role\": \"user\", \"content\": " + pre + charbuf + "\"}"
                        body = "{\"model\": \"gpt-4o-mini\", \"messages\": [" + b1 + ", " + b2 + "]}"
                        requestr = "{\"custom_id\": \"request_" + str(request_num) + "\", \"method\": \"POST\", \"url\": \"/v1/chat/completions\", \"body\": " + body + "}"
                        fout.write(requestr + "\n")
                        charbuf = ""
                        request_num = request_num + 1
                    request_num = request_num + 1
                else:
                    charbuf = charbuf + line.strip().replace("\"", "\\\"") + "\\n"
                if len(charbuf) > 3000:
                    b1 = "{\"role\": \"system\", \"content\": \"" + sysprompt + "\"}"
                    b2 = "{\"role\": \"user\", \"content\": " + pre + charbuf + "\"}"
                    body = "{\"model\": \"gpt-4o-mini\", \"messages\": [" + b1 + ", " + b2 + "]}"
                    requestr = "{\"custom_id\": \"request_" + str(request_num) + "\", \"method\": \"POST\", \"url\": \"/v1/chat/completions\", \"body\": " + body + "}"
                    fout.write(requestr + "\n")
                    charbuf = ""
                    request_num = request_num + 1
            if len(charbuf.strip()) > 0:
                b1 = "{\"role\": \"system\", \"content\": \"" + sysprompt + "\"}"
                b2 = "{\"role\": \"user\", \"content\": " + pre + charbuf + "\"}"
                body = "{\"model\": \"gpt-4o-mini\", \"messages\": [" + b1 + ", " + b2 + "]}"
                requestr = "{\"custom_id\": \"request_" + str(request_num) + "\", \"method\": \"POST\", \"url\": \"/v1/chat/completions\", \"body\": " + body + "}"
                fout.write(requestr + "\n")
                request_num = request_num + 1
                charbuf = ""

with open("./bin/chapters.jsonl", "w") as fout:
    for file in glob.glob(glob.escape(dirout) + "/*"):
        with open(file, "r") as fin:
            for line in fin:
                if len(line) > 0:
                    fout.write(line)