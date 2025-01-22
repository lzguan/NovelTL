import os
import shutil
from google.cloud import vision
import re
import glob

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../vision-api-key.json'
WORD = re.compile(r"\w+")

client = vision.ImageAnnotatorClient()

def detect_text(path):
    with open(path, "rb") as image_file:
        content = image_file.read()
    
    image = vision.Image(content = content)

    response = client.document_text_detection(image = image)
    document = response.full_text_annotation
    out_text = ""
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        out_text = out_text + symbol.text
                    out_text = out_text + " "
            out_text = out_text + "\n"
    return out_text

detect_text("image.jpg")

dirs = []

for dirname in glob.glob("chapter*-*"):
    dirs.append(dirname)
dirs = dirs[12:]
print(dirs)

count = 0

for dir in dirs:
    try:
        if os.path.exists(dir + "/cloudvision"):
            shutil.rmtree(dir + "/cloudvision")
        os.mkdir(dir + "/cloudvision")
    except OSError as e:
        print("Error deleting " + dir + "/cloudvision: " + e.strerror)
        continue
    for filename in glob.glob(glob.escape(dir) + "/img/*.jpg"):
        if count % 7 == 0:
            print("Processing " + filename)
            count = 0
        elif count % 7 == 1:
            print("...")
        result  = detect_text(filename)
        fname = os.path.basename(filename)
        fout = open(dir + "/cloudvision/" + fname[:-4] + "_kr.txt", 'w')
        fout.write(result + "\n")
        fout.close()
        count = count + 1
    print("Done processing " + dir)