import retrieve_gpt
import send_gpt
import time

bin = "bin/"

for i in range(8,25):
    send_gpt.send_gpt(bin + "glossary_bin_" + str(i) + ".jsonl", bin + "batchresponse_" + str(i) + ".json")
    retrieved = False
    while not retrieved:
        time.sleep(60)
        retrieved = retrieve_gpt.retrieve_gpt(bin + "batchresponse_" + str(i) + ".json", bin + "glossary_translated_" + str(i) + ".jsonl")