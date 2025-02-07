import requests
import os
from pyquery import PyQuery

outfolder = "../../../Database/secretsoftheworld/raw/"
baseUrl = "https://ncode.syosetu.com/"
curUrl = "n6868ew/1/"

chapter = 1

while True:
    print(baseUrl + curUrl)
    r = requests.get(baseUrl + curUrl, headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'
    })

    html = r.text
    pq = PyQuery(html)

    next = pq('a.c-pager__item--next')
    curUrl = next('a').attr('href')

    content = pq('div.p-novel__text')
    def e(q):
        if q.text:
            return q.text.strip()
        return ""
    contentText = [e(p) for p in content.find('p')]

    title = pq('div.p-novel__subtitle-episode')
    titleText = title[0].text.strip()

    with open(outfolder + "chapter_" + str(chapter) + ".txt", "w") as out:
        out.write(titleText + "\n")
        for c in contentText:
            out.write(c + "\n")
    chapter = chapter + 1
    if not next:
        break