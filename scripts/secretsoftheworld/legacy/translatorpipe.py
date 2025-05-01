import retrieve_gpt
import send_gpt
import time

bin = "bin/"

# send_gpt.send_gpt("translate_request.jsonl", bin + "batchresponse_translate.json")
retrieve_gpt.retrieve_gpt(bin + "batchresponse_translate.json", "novel_translated.jsonl")