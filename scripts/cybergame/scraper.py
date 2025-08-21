# Scraper for zhenhunxiaoshuo.com

import requests
import os
from pyquery import PyQuery
import time

outfolder = "../../../Database/cybergame/raw/" # output directory
nextUrl = "https://www.zhenhunxiaoshuo.com/256864.html" # url of first chapter

chapter = 207 # starting chapter num
strikes = 0
delay = 5

def process(html):
    pq = PyQuery(html)

    titleText = pq('h1.article-title').text()

    content = pq('article.article-content')
    paragraphs = content('p')
    contentText = [p.text() for p in paragraphs.items()]

    next = pq('span.article-nav-next')
    nextUrl = next('a').attr('href')

    return titleText, contentText, nextUrl

while True:
    temp = nextUrl
    print(f'chapter: {chapter} {nextUrl}')
    r = requests.get(nextUrl, headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'
    })

    html = r.text
    titleText, contentText, nextUrl = process(html)
    with open(outfolder + "chapter_" + str(chapter) + ".txt", "w") as out:
        out.write(titleText + "\n")
        for c in contentText:
            out.write(c + "\n")
    if strikes > 4:
        break
    if not nextUrl:
        strikes = strikes + 1
        nextUrl = temp
        print('failed to get nexturl')
        time.sleep(delay)
        delay = delay * 2
    else:
        chapter = chapter + 1
        strikes = 0
        delay = 5
