import retrieve_gpt
import send_gpt

bin = "bin/"

retrieve_gpt.retrieve_gpt(bin + "batchresponse.json", bin + "glossary_translated.jsonl")
