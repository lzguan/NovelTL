import json
from openai import OpenAI

client = OpenAI(base_url = "https://api.deepseek.com")

infile = 'glossary_edited.json'
outfile = 'glossary_translated.csv'
rawdir = '../../../Database/sheisnotawitch/raw/'

userprompt = "I will give you a list of words separated by newlines, along with a chapter of a Chinese fantasy webnovel. Translate these words as they appear in the novel and output ONLY the ENGLISH names of the terms, separated by newlines. \nList:\n"

out = {}
MAX_FAIL = 40
fails = 0

with open(infile, 'r') as f, open(outfile, 'w') as g:
    glossary = json.load(f)
    for key in glossary:
        while fails < MAX_FAIL:
            try:
                words = ""
                for word in glossary[key]:
                    words = words + word + "\n"
                with open(rawdir + "chapter_" + key + ".txt", 'r') as h:
                    chapter = h.read()
                response = client.chat.completions.create(
                    model = "deepseek-chat",
                    messages = [{"role": "system", "content": "You are a translator making a glossary of names for a chinese fantasy webnovel called \"才不是魔女\"."}, {"role": "user", "content": userprompt + words + "\nChapter:" + chapter}]
                )
                print("response " + key + " received")
                rmsg = response.choices[0].message.content
                tl_words =rmsg.splitlines()
                i = 0
                wstr = ""
                for word in glossary[key]:
                    wstr = word + ", " + tl_words[i] + "\n"
                    i = i + 1
                g.write(wstr)
                break
            except:
                print("An error occured")
        if fails >= MAX_FAIL:
            print("Too many fails, breaking at chapter " + key)
            break
    json.dump(out, g)
    



# print(response)