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
from BaseParser import BaseParser
from model.Nengo import setnengo
from model.Nengo import getdatefromwareki
from model.Session import setsession

class IndexParser(BaseParser):

    links = []
    sess = None

    def parse(self, url):
        self.links = []
        BaseParser.parse(self, url)

    def handle_starttag(self, tag, method, attributes):
        '/vote_ind.htm'
        if tag == "a":
            for attr in attributes:
                if attr[0] == "href" and attr[1].endswith('/vote_ind.htm'):
                    if 0 <= attr[1].find("://"):
                        self.href = attr[1]
                    else:
                        self.href = self.base + attr[1]

    def handle_endtag(self, tag, method):
        if tag == "a":
            self.href = ""
        elif tag == "tr":
            self.sess = None

    def handle_data(self, data):
        if self.href != "" and data == "投票結果":
            self.links.append(self.href)
        elif 0 < data.find("年（") and 0 < data.find("年）", data.find("年（")):
            setnengo(unicode(data, "utf8"))
            text = unicode(data, "utf8")
            if 0 < text.find(u"～") and self.sess != None:
                start = getdatefromwareki(text[:text.find(u"～")])
                if 0 < text.find(u"（", text.find(u"～") + 1):
                    end = getdatefromwareki(text[text.find(u"～")+1:text.find(u"（", text.find(u"～"))])
                else:
                    end = getdatefromwareki(text[text.find(u"～")+1:])
                if self.sess.start != start and self.sess.end != end:
                    self.sess.start = start
                    self.sess.end = end
                    self.sess.put()
        elif data.startswith("第") and data.endswith("回国会"):
            self.sess = setsession(unicode(data, "utf8"))
        elif data.startswith(" 第") and data.endswith("回国会"):
            self.sess = setsession(unicode(data, "utf8"))
        elif 0 <= data.find("常会"):
            if self.sess != None and self.sess.sort != u"常会":
                self.sess.sort = u"常会"
                self.sess.put()
        elif 0 <= data.find("特別会"):
            if self.sess != None and self.sess.sort != u"特別会":
                self.sess.sort = u"特別会"
                self.sess.put()
        elif 0 <= data.find("臨時会"):
            if self.sess != None and self.sess.sort != u"臨時会":
                self.sess.sort = u"臨時会"
                self.sess.put()
