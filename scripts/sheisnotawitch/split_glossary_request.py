infile = "glossary_request.jsonl"
bin = "bin/"
count = 0
i = 0
out = open(bin + "glossary_request_bin_" + str(count) + ".jsonl", 'w')
with open(infile, 'r') as f:
    for line in f:
        out.write(line)
        if i == 20:
            out.close()
            i = 0
            count = count + 1
            out = open(bin + "glossary_bin_" + str(count) + ".jsonl", 'w')
        i = i + 1
out.close()