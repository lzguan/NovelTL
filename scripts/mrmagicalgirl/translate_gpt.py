from openai import OpenAI
import json

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True

bindir = "bin"
linenum = 0
with open(bindir + "/chapters.jsonl", "r") as fin:
    for line in fin:
        if not is_json(line):
            print("FAILED at line number " + str(linenum))
            exit()
        linenum = linenum + 1

client = OpenAI()

uploadresponse = client.files.create(file = open(bindir + "/chapters.jsonl", "rb"), purpose = "batch")

batchresponse = client.batches.create(input_file_id = uploadresponse.id, endpoint = "/v1/chat/completions", completion_window = "24h")

with open(bindir + "/batchresponse.json", "w") as fout:
    json.dump(json.dumps(batchresponse, default=lambda o: o.__dict__), fout)