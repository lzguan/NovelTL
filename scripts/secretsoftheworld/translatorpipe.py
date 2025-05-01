import json
import glob
import os
from openai import OpenAI

client = OpenAI(base_url = "https://api.deepseek.com")

glossaryfile = 'glossary_translated.csv'
rawdir = '../../../Database/secretsoftheworld/raw/'
outdir = '../../../Database/secretsoftheworld/en/'

userprompt = "Translate the following chapter into English. For terms in the glossary, use the glossary to translate them. Mantain the original style of the author when appropriate.\n"
sysprompt = "You are a translating a Japanese webnovel called \"世界の秘密を教えてあげる\" to english. It is a romance fantasy novel. Do not add any additional text. A glossary of terms appearing in this chapter is listed below (if there are any) in the format \"Japanese name\": \"English name\":\n"

glossary = {}
with open(glossaryfile, 'r') as gf:
    for line in gf:
        ln = line.strip('\n').split(",")
        glossary[ln[0]] = ln[1]

out = {}
MAX_FAIL = 40
fails = 0


for cnum in range(7, 97):
    gcur = ""
    file = rawdir + "chapter_" + str(cnum) + ".txt"
    with open(file, 'r') as f:
        chap = f.read()
    for key in glossary:
            if key in chap:
                gcur = gcur + key + ": " + glossary[key] + "\n"
    while fails < MAX_FAIL:
        try:
            response = client.chat.completions.create(
                model = "deepseek-chat",
                messages = [{"role": "system", "content": sysprompt + gcur}, {"role": "user", "content": userprompt + chap}],
                temperature = 1.3
            )
            print("Translated " + file)
            break
        except Exception as e:
            print("An error occured")
            print(e)
    if fails >= MAX_FAIL:
        print("Too many fails, breaking at " + file)
        break
    with open(outdir + os.path.basename(file), 'w') as g:
        g.write(response.choices[0].message.content)
