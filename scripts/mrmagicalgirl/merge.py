from PIL import Image
import glob
import os

dirs = []

for dirname in glob.glob("chapter*-*"):
    dirs.append(dirname)

print(dirs)

for dir in dirs:
    for filename in glob.glob(glob.escape(dir) + "/img/*.gif"):
        print(filename)
        img = Image.open(filename).convert('RGB')
        if os.path.isfile(filename[:-4] + "jpg"):
            raise ValueError('oh no')
        img.save(filename[:-4] + ".jpg")
        os.remove(filename)
