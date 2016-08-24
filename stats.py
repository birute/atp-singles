# -*- coding: utf-8 -*- 

# How to:

# 1. Run "tours.py" to get all 86 tournaments from ATP Singles list
# 2. Run "archive.py" to get historical links (247) from past ~ 4 years i.e. 2012-2016
# 3. Run "games.py" to get all links from the tournaments
# 4. Run "stats.py" to get all stats

import sys
import requests
import re
from lxml import html
import json
import itertools
import numpy as np
import pandas as pd
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
    if(len(urls) > 0):
        r = Render(urls.pop())
        timer.start(500)
    else:
        print("finished")
        sys.exit(app.exec_())

def check_done():
    global r, timer, urls

    if r.frame is not None:
        timer.stop()
        html_result = r.frame.toHtml()
        formatted_result = str(html_result.toAscii())
        tree = html.fromstring(formatted_result)
        time = tree.xpath("//td[@class='mstat-date']//text()")
        Service = 'Service'
        Score = 'Score'
        match = tree.xpath("//td[@class='h-part']//text()")[0:2]
        table = {}

        # xpath rules ...
        try:
            if Service in match or Score in match and time[0][-5:] != "00:00":
                table["link"] = "True"
                table["tournament_name"] = tree.xpath("//div[@class='fleft']//a//text()")
                players = tree.xpath("//span[@class='tname']//a//text()")
                player_rankA = tree.xpath("//td[@class='tface-home']//span[@class='participant-detail-rank']//text()")
                player_rankB = tree.xpath("//td[@class='tface-away']//span[@class='participant-detail-rank']//text()")
                if len(player_rankA) > 0:
                    table["atp_A"] = re.sub("[^0-9]", "", player_rankA[1])
                else:
                    table["atp_A"] = ""

                if len(player_rankB) > 0:
                    table["atp_B"] = re.sub("[^0-9]", "", player_rankB[1])
                else:
                    table["atp_B"] = ""
                
                table["playerA"] = players[0]
                table["playerB"] = players[1]
                print players[0]
                print players[1]

                score = tree.xpath("//span[@class='scoreboard']//text()")

                if len(score) > 0:
                    table["scoreA"] = score[0]
                    table["scoreB"] = score[1]
                    if score[0] > score[1]:
                        table["winner"] = "A win"
                    else:
                        table["winner"] = "B win"
                else:
                    table["scoreA"] = ""
                    table["scoreB"] = ""
                    table["winner"] = ""                  

                table["time"] = time
                odds = tree.xpath("//td[contains(@class, 'kx')]//span//text()")
                print odds

                if len(odds) > 2:
                    table["oddsA"] = odds[2]
                    table["oddsB"] = odds[3]
                else:
                    table["oddsA"] = ""
                    table["oddsB"] = ""                    

                # main stats table
                labels = tree.xpath("//td[@class='score stats']//text()")
                left = tree.xpath("//div[@style='float: left;']//text()")
                right = tree.xpath("//div[@style='float: right;']//text()")

                key = "Aces"
                if key in labels:
                    table["acesA"] = left[labels.index(key)]
                    table["acesB"] = right[labels.index(key)]
                else:
                    table["acesA"] = "NA"
                    table["acesB"] = "NA"

                key = "Double Faults"
                if key in labels:
                    table["dfA"] =  left[labels.index(key)]
                    table["dfB"] = right[labels.index(key)]
                else:
                    table["dfA"] = "NA"
                    table["dfB"] = "NA"

                key = "1st Serve Percentage"
                if key in labels:
                    table["fsppA"] =  left[labels.index(key)]
                    table["fsppB"] = right[labels.index(key)]
                else:
                    table["fsppA"] = "NA"
                    table["fsppB"] = "NA"

                key = "1st Serve Points Won"
                if key in labels:
                    table["fspA"] =  left[labels.index(key)]
                    table["fspB"] = right[labels.index(key)]
                else:
                    table["fspA"] = "NA"
                    table["fspB"] = "NA"

                key = "2nd Serve Points Won"
                if key in labels:
                    table["sspA"] =  left[labels.index(key)]
                    table["sspB"] = right[labels.index(key)]
                else:
                    table["sspA"] = "NA"
                    table["sspB"] = "NA"         

                key = "Break Points Saved"
                if key in labels:
                    table["bpsA"] =  left[labels.index(key)]
                    table["bpsB"] = right[labels.index(key)]
                else:
                    table["bpsA"] = "NA"
                    table["bpsB"] = "NA"  

                key = "1st Return Points Won"
                if key in labels:
                    table["frpA"] =  left[labels.index(key)]
                    table["frpB"] = right[labels.index(key)]
                else:
                    table["frpA"] = "NA"
                    table["frpB"] = "NA"  

                key = "2nd Return Points Won"
                if key in labels:
                    table["srpA"] =  left[labels.index(key)]
                    table["srpB"] = right[labels.index(key)]
                else:
                    table["srpA"] = "NA"
                    table["srpB"] = "NA"  

                key = "Break Points Converted"
                if key in labels:
                    table["bpcA"] =  left[labels.index(key)]
                    table["bpcB"] = right[labels.index(key)]
                else:
                    table["bpcA"] = "NA"
                    table["bpcB"] = "NA"  

                key = "Max Points In Row"
                if key in labels:
                    table["mprA"] =  left[labels.index(key)]
                    table["mprB"] = right[labels.index(key)]
                else:
                    table["mprA"] = "NA"
                    table["mprB"] = "NA"  

                key = "Service Points Won"
                if key in labels:
                    table["spwA"] =  left[labels.index(key)]
                    table["spwB"] = right[labels.index(key)]
                else:
                    table["spwA"] = "NA"
                    table["spwB"] = "NA"  

                key = "Return Points Won"
                if key in labels:
                    table["rpwA"] =  left[labels.index(key)]
                    table["rpwB"] = right[labels.index(key)]
                else:
                    table["rpwA"] = "NA"
                    table["rpwB"] = "NA"  

                key = "Total Points Won"
                if key in labels:
                    table["tpwA"] =  left[labels.index(key)]
                    table["tpwB"] = right[labels.index(key)]
                else:
                    table["tpwA"] = "NA"
                    table["tpwB"] = "NA"  

                key = "Max Games In Row"
                if key in labels:
                    table["mgrA"] =  left[labels.index(key)]
                    table["mgrB"] = right[labels.index(key)]
                else:
                    table["mgrA"] = "NA"
                    table["mgrB"] = "NA"  

                key = "Service Games Won"
                if key in labels:
                    table["sgwA"] =  left[labels.index(key)]
                    table["sgwB"] = right[labels.index(key)]
                else:
                    table["sgwA"] = "NA"
                    table["sgwB"] = "NA"  

                key = "Return Games Won"
                if key in labels:
                    table["rgwA"] =  left[labels.index(key)]
                    table["rgwB"] = right[labels.index(key)]
                else:
                    table["rgwA"] = "NA"
                    table["rgwB"] = "NA"  

                key = "Total Games Won"
                if key in labels:
                    table["tgwA"] =  left[labels.index(key)]
                    table["tgwB"] = right[labels.index(key)]
                else:
                    table["tgwA"] = "NA"
                    table["tgwB"] = "NA"

                df = pd.DataFrame(table)
                print df
                df.to_csv("test.csv", index = False, mode = 'a', columns = 
                    ['link','tournament_name','playerA', 'playerB', 'atp_A', 'atp_B', 'scoreA', 'scoreB', 'winner',
                     'time', 'oddsA', 'oddsB', 'acesA', 'acesB', 'dfA', 'dfB', 'fsppA', 'fsppB', 'fspA', 'fspB','sspA', 'sspB', 'bpsA','bpsB', 'frpA', 'frpB', 
                     'srpA', 'srpB', 'bpcA', 'bpcB', 'mprA', 'mprB', 'spwA', 'spwB', 'rpwA', 'rpwB', 'tpwA', 'tpwB', 'mgrA', 
                     'mgrB', 'sgwA', 'sgwB', 'rgwA', 'rgwB', 'tgwA', 'tgwB'])
            else:
                pass
                print("empty")
            go_again()

        except IndexError, ValueError:
            pass

app = QApplication(sys.argv)

with open('urls.txt') as data:
    urls = json.load(data)

timer = QTimer()
timer.timeout.connect(check_done)

go_again()
sys.exit(app.exec_())
