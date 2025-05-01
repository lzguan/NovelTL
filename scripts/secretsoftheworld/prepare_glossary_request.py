import json
import os
import shutil
import glob

sysprompt = "You are a translator making a glossary of names for a japanese slice of life fantasy webnovel called \\\"世界の秘密を教えてあげる\\\"."
prompt = "I will give you a list of words separated by spaces, along with a chapter of a japanese fantasy webnovel. Please translate these words as they appear in the novel. Only output the English names of the terms, separated by newlines. If the term does not appear in the text, output ERROR instead.\\nList:\\n"

with open('glossary.txt', 'r') as f, open('glossary_request.jsonl', 'w') as g:
    for line in f:
        bits = line.split(maxsplit=1)
        chap = bits[0][:-1]
        words = bits[1].rstrip() + "\\n"
        chapter = ""
        with open('../../../Database/secretsoftheworld/raw/chapter_' + chap + '.txt', 'r') as h:
            for line in h:
                chapter = chapter + line.rstrip().replace("\"","\\\"") + "\\n"
        b1 = "{\"role\": \"system\", \"content\": \"" + sysprompt + "\"}"
        b2 = "{\"role\": \"user\", \"content\": \"" + prompt + words + "Chapter:\\n" + chapter + "\"}"
        body = "{\"model\": \"gpt-4o\", \"messages\": [" + b1 + ", " + b2 + "]}"
        requestr = "{\"custom_id\": \"request_" + chap + "\", \"method\": \"POST\", \"url\": \"/v1/chat/completions\", \"body\": " + body + "}"
        g.write(requestr + "\n")