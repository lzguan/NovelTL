import fileinput
import glob
import time
import deepl


dirs = ["test"]
ocr = "cloudvision"

translator = deepl.Translator("4bd5e0d3-c7d7-449b-b69c-15fee01875ab:fx")

for dir in dirs:
    blocks = 0
    fout = open(dir + "/" + ocr + "/" + dir + "_en.txt", 'w')
    charbuf = ""
    charcnt = 0

    for filename in glob.glob(glob.escape(dir) + "/" + ocr + "/*_kr.txt"):
        finput = fileinput.input(filename)
        
        for line in finput:
            charbuf = charbuf + line + "\n"
            charcnt = charcnt + len(line) + 1
            
        if charcnt > 4000:
            oot = translator.translate_text(charbuf, target_lang = "EN-US")
            print("Translated block " + str(blocks) + ": " + str(charcnt) + " characters")
            charcnt = 0
            charbuf = ""
            blocks = blocks + 1

            if oot != None:
                fout.write(oot.text + "\n")
            time.sleep(5)
    if charbuf != "":
        oot = translator.translate_text(charbuf, target_lang = "EN-US")
        print("Translated block " + str(blocks) + ": " + str(charcnt) + " characters")
        if oot != None:
            fout.write(oot.text + "\n")

        