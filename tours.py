# -*- coding: utf-8 -*- 

# How to:

# 1. Run "tours.py" to get all 86 tournaments from ATP Singles list
# 2. Run "archive.py" to get historical links (247) from past ~ 4 years i.e. 2012-2016
# 3. Run "games.py" to get each game stats from player A and B

from lxml import html
import json
import time
import re
import itertools
import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  

reload(sys)
sys.setdefaultencoding("utf-8")

base = 'http://www.flashscore.com/tennis/'
baser = 'http://www.flashscore.com'

# PyQt4
class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()

  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()

# 75+ ATP 'singles' tournament hrefs
def tour():
    r = Render(base)  
    result = r.frame.toHtml()
    formatted_result = str(result.toAscii())
    tree = html.fromstring(formatted_result)
    tour = tree.xpath("//li[@id='lmenu_5724']//@href")[1:]
    tour = [baser + str(x) for x in tour]
    arch = [str(x) + 'archive/' for x in tour]

# Saving hrefs with 'archive' extension to 'tour.txt'
    with open('tour.txt', 'w+') as outfile:
        json.dump(arch, outfile, indent=4, sort_keys=True, separators=(',', ':'))
    print "Number of tournaments: ", len(arch)

# Get all tournaments
tour()

