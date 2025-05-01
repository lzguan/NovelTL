from openai import OpenAI
import json
from pprint import pprint
import sys

client = OpenAI()

def retrieve_gpt(response, output):
    with open(response, "r") as fin:
        batchresponse = json.loads(json.load(fin))
    batchreturn = client.batches.retrieve(batchresponse['id'])
    if batchreturn.status == 'completed':
        print("Retrieving file " + batchreturn.output_file_id)
        outputf = client.files.content(batchreturn.output_file_id)
        with open(output, "w") as fout:
            fout.write(outputf.text)
        outputf.close()
        return True
    else:
        print("Error: batch not completed yet.")
        print("Status: " + batchreturn.status)
        print(batchreturn.request_counts)
        return False