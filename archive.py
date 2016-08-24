# -*- coding: utf-8 -*- 

# How to:

# 1. Run "tours.py" to get all 86 tournaments from ATP Singles list
# 2. Run "archive.py" to get historical links (247) from past ~ 4 years i.e. 2012-2016
# 3. Run "games.py" to get each game stats from player A and B

import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl, QTimer
from PyQt4.QtWebKit import QWebPage
import requests
import re
from lxml import html
import json

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
        print("loading",urls)
        r = Render(urls.pop())
        timer.start(500)
    else:
        print("finished")
        sys.exit(app.exec_())

full = []
def check_done():
    global r, timer
    if r.frame is not None:
        timer.stop()
        html_result = r.frame.toHtml()
        formatted_result = str(html_result.toAscii())
        tree = html.fromstring(formatted_result)
        seasons = tree.xpath("//tbody//td//@href[contains(.,'/tennis/')]")
        seasons = [baser + str(x) for x in seasons]
        if len(seasons) < 2:
            years = seasons
        else:
            years = seasons[0:3]
        print years
        full.append(years)
        with open('tour_year.txt', 'w+') as outfile:
            link = reduce(lambda x,y: x+y, full)
            json.dump(link, outfile, indent=4, sort_keys=True)
        print("loaded")
        go_again()

app = QApplication(sys.argv)

# load trnments
with open('tour.txt') as data:
	urls = json.load(data)

timer = QTimer()
timer.timeout.connect(check_done)

go_again()
sys.exit(app.exec_())
