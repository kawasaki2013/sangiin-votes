#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
sangiin-votes

Copyright 2011 Michinobu Maeda.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: Michinobu Maeda
'''
import datetime
import hashlib
import logging
from model import utils
from model.VoteItem import VoteItem
from model.VoteItemParty import VoteItemParty
from BaseParser import BaseParser

class VoteParser(BaseParser):
    
    sess = None
    item = None
    party = None
    content = False
    title = False
    date = None
    
    def __init__(self, sess):
        BaseParser.__init__(self)
        self.sess = sess
        self.item = None
        self.party = None
        self.content = False
        self.title = False
        self.date = None

    def handle_starttag(self, tag, method, attributes):
        if tag == "h1":
            self.content = True

    def handle_endtag(self, tag, method):
        pass

    def handle_data(self, data):
        if self.content == False:
            pass
        elif 0 <= data.find("年") and data.find("年") < data.find("月") and data.find("月") < data.find("日"):
            text = unicode(data, "utf8")
            text = utils.numzentohan(text)
            text = utils.erasewhitespace(text)
            if text.startswith(u"1") or text.startswith(u"2"):
                year = int(text[:text.find(u"年")])
                mon = int(text[text.find(u"年")+1:text.find(u"月")])
                day = int(text[text.find(u"月")+1:text.find(u"日")])
                self.date = datetime.date(year, mon, day)
        elif 0 <= data.find("投票総数") and data.find("投票総数") < data.find("賛成票") and data.find("賛成票") < data.find("反対票"):
            text = unicode(data, "utf8")
            text = utils.numzentohan(text)
            text = utils.erasewhitespace(text)
            self.item.total = int(text[text.find(u"投票総数")+4:text.find(u"賛成票")])
            self.item.aye = int(text[text.find(u"賛成票")+3:text.find(u"反対票")])
            if 0 < text.find(u"【"):
                self.item.nay = int(text[text.find(u"反対票")+3:text.find(u"【")])
            else:
                self.item.nay = int(text[text.find(u"反対票")+3:])
            self.item.put()
            logging.info(str(self.item.date) + ":" + str(self.item.total) + "/" + str(self.item.aye) + "/" + str(self.item.nay) + ":" + self.item.name[:20])
        elif self.item == None and 0 <= data.find("案件名："):
            self.title = True
        elif self.item == None and self.title == True:
            text = unicode(data, "utf8")
            if 0 < len(text):
                timetable = ""
                handling = ""
                if 0 < text.find(u"　"):
                    timetable = text[:text.find(u"　")]
                    text = text[text.find(u"　")+1:]
                if 0 < text.rfind(u"（") and text.endswith(u"）"):
                    handling = text[text.rfind(u"（"):]
                    text = text[:text.rfind(u"（")]
                key = hashlib.sha1(text.encode("utf8")).hexdigest()
                self.item = VoteItem(parent=self.sess, key_name=key, name=text, date=self.date)
                self.item.timetable = timetable
                self.item.handling = handling
                self.title = False
        elif self.item == None:
            pass
        elif 0 <= data.find("(") and  0 <= data.find("名)", data.find("(")):
            text = unicode(data, "utf8")
            text = utils.numzentohan(text)
            text = utils.erasewhitespace(text)
            name = text[:text.find(u"(")]
            total = int(text[text.find(u"(")+1:text.find(u"名)")])
            self.party =VoteItemParty(parent=self.item, key_name=name, total=total)
        elif self.party != None and 0 <= data.find("賛成票") and 0 <= data.find("反対票", data.find("賛成票")):
            text = unicode(data, "utf8")
            text = utils.numzentohan(text)
            text = utils.erasewhitespace(text)
            self.party.aye = int(text[text.find(u"賛成票")+3:text.find(u"反対票")])
            self.party.nay = int(text[text.find(u"反対票")+3:])
            self.party.put()
