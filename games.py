# -*- coding: utf-8 -*- 

# How to:

# 1. Run "tours.py" to get all 86 tournaments from ATP Singles list
# 2. Run "archive.py" to get historical links (247) from past ~ 4 years i.e. 2012-2016
# 3. Run "games.py" to get all links from the tournaments
# 4. Run "stats.py" to get all statistics

import sys
import requests
import re
from lxml import html
import json
import itertools
import numpy as np
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl, QTimer
from PyQt4.QtWebKit import QWebPage

reload(sys)
sys.setdefaultencoding("utf-8")

base = 'http://www.flashscore.com/tennis/'
baser = 'http://www.flashscore.com'

class Render(QWebPage):
    def __init__(self, url):
        QWebPage.__init__(self)
        self.frame = None
        self.mainFrame().loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))

    def _loadFinished(self, result):
        self.frame = self.mainFrame()

def go_again():
    global r, timer, urls
    if(len(urls)>0):
        r = Render(urls.pop())
        timer.start(500)
    else:
        print("finished")
        sys.exit(app.exec_())

def check_done():
    global r, timer, hashes
    hashes_links = []
    if r.frame is not None:
        timer.stop()
        
        html_result = r.frame.toHtml()
        formatted_result = str(html_result.toAscii())
        tree = html.fromstring(formatted_result)
        main = tree.xpath("//div[@id='tournament-page-data-results']//text()")
        start = [match.start() for match in re.finditer(re.escape("AA"), str(main))]
        start = [6 + x for x in start]
        stop = [8 + x for x in start]

        # get hash links
        hashes = []
        for st, stp in itertools.izip(start, stop):
            code = str(main)[int(st):int(stp)]
            res =  re.search('[A-Za-z0-9]+', code).group(0)
            if len(res) > 7:
                hasher = baser + '/match/' +  str(res) + '/#match-statistics;0'
                hashes.append(hasher)
        with open('urls.txt', 'a') as outfile:
            json.dump(hashes, outfile, indent=4, sort_keys=True)
        print hashes
        print("loaded")
        go_again()


app = QApplication(sys.argv)

with open('tour_year.txt') as data:
    urls = [str(x) + 'results/' for x in json.load(data)]
    urls = urls

timer = QTimer()
timer.timeout.connect(check_done)

go_again()
sys.exit(app.exec_())
