from openai import OpenAI
import json
import sys

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True

bindir = "bin"
linenum = 0
with open('glossary_bin.jsonl', 'r') as fin:
    for line in fin:
        json.loads(line)
        linenum = linenum + 1

client = OpenAI()

uploadresponse = client.files.create(file = open(bindir + "/glossary_bin_" + str(sys.argv[1]) + ".jsonl", "rb"), purpose = "batch")

batchresponse = client.batches.create(input_file_id = uploadresponse.id, endpoint = "/v1/chat/completions", completion_window = "24h")

with open(bindir + "/batchresponse_" + str(sys.argv[1]) + ".json", "w") as fout:
    json.dump(json.dumps(batchresponse, default=lambda o: o.__dict__), fout)