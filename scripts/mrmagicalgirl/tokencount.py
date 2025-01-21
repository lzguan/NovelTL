import tiktoken
import glob

total_count = 0

# Choose the model (e.g., "gpt-4", "gpt-3.5-turbo")
model = "gpt-4o-mini"

# Load the appropriate tokenizer
def count_tokens(text, model):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

for file in glob.glob("chapters_all/*.txt"):
    # Define the text to analyze
    with open(file, "r", encoding="utf-8") as file:
        text = file.read()
    # Get the token count
    token_count = count_tokens(text, model)
    print(f"{file.name}: Number of tokens for {model}: {token_count}")
    total_count = total_count + token_count

print(f"Total count: {total_count}")




