from openai import OpenAI
import json
from pprint import pprint

client = OpenAI()
bindir = "bin"

with open(bindir + "/batchresponse.json", "r") as fin:
    batchresponse = json.loads(json.load(fin))

batchreturn = client.batches.retrieve(batchresponse['id'])

if batchreturn.status == 'completed':
    print("Retrieving file " + batchreturn.output_file_id)
    outputf = client.files.content(batchreturn.output_file_id)
    with open(bindir + "/chapters_translated.jsonl", "w") as fout:
        fout.write(outputf.text)
    outputf.close()
else:
    print("Error: batch not completed yet.")
    print("Status: " + batchreturn.status)
    print(batchreturn.request_counts)