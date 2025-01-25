from openai import OpenAI
import json
import sys

client = OpenAI()

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True

def send_gpt(input, response):
    uploadresponse = client.files.create(file = open(input, "rb"), purpose = "batch")
    batchresponse = client.batches.create(input_file_id = uploadresponse.id, endpoint = "/v1/chat/completions", completion_window = "24h")
    with open(response, "w") as fout:
        json.dump(json.dumps(batchresponse, default=lambda o: o.__dict__), fout)