import glob
import os
import shutil

indir  = "chapters_all_en"
outdir = "chapters_all_en_html"

try:
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
except OSError as e:
    print("Delete " + outdir + " failed: " + e.strerror)
    exit(1)

for file in glob.glob(glob.escape(indir) + "/*.txt"):
    template_1 = """<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """

    title = ""
    template_2 = """
  </head>
  <body>
    <section>
      <button class="previous">Previous</button>
      <button class="next">Next</button>
    </section>
    """
    title_text = ""
    paragraph_text = ""
    outstr = template_1
    is_first = True
    template_3 = """
    </section>
    <section>
      <button class="previous">Previous</button>
      <button class="next">Next</button>
    </section>
    <script>
      const script = document.createElement('script');
      script.src = 'http://localhost:3000/src/js/src.js';
      script.type = 'text/javascript';
      script.onload = () => {
        console.log('Loaded src.js');
      };
      script.onerror = () => {
        console.error('Error loading src.js');
      };
      document.head.appendChild(script)
    </script>
  </body>
</html>
"""
    with open(file, "r") as fin:
        for line in fin:
            if is_first:
                title_text = """<section>
      <h3>{line}</h3>
    </section>
    <section>
""".format(line=line.strip())
                title = """<title>{line}</title>""".format(line=line.strip())
                outstr = outstr + title + template_2 + title_text
                is_first = False
            elif len(line) > 7 and line[0:7] == "__IMG__":
                outstr = outstr + "      <img id=\"" + line.strip()[7:] + "\" alt=\"Image could not be loaded\">"
            else:
                outstr = outstr + "      <p>" + line.strip() + "</p>\n"
        outstr = outstr + template_3
    with open(outdir + "/" + os.path.basename(file[:-4] + ".html"), "w") as fout:
        fout.write(outstr)