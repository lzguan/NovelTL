import requests
import os
from pyquery import PyQuery

outfolder = "../../../Database/sheisnotawitch/raw/"
baseUrl = "http://www.biquge5200.net/"
curUrl = "140_140086/176332920.html"

chapter = 0

while True:
    r = requests.get(baseUrl + curUrl)

    html = r.text
    pq = PyQuery(html)

    next = pq('a:contains("下一章")')
    if not next:
        break
    curUrl = next('a').attr('href')

    content = pq('div#content')
    contentText = [p.text.strip() for p in content.find('p')]

    title = pq('div.bookname h1')
    titleText = title[0].text.strip()

    with open(outfolder + "chapter_" + str(chapter) + ".txt", "w") as out:
        out.write(titleText + "\n")
        for c in contentText:
            out.write(c + "\n")
    chapter = chapter + 1