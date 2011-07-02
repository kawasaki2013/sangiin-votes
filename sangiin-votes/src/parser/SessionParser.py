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
from model import utils
from model.Session import Session

class SessionParser(BaseParser):

    links = []
    sess = None

    def parse(self, url):
        self.links = []
        BaseParser.parse(self, url)

    def handle_starttag(self, tag, method, attributes):
        if tag == "a":
            for attr in attributes:
                if attr[0] == "href" and 0 > attr[1].find("/") and 0 <= attr[1].find(".htm"):
                    self.links.append(self.base + attr[1])

    def handle_endtag(self, tag, method):
        if tag == "a":
            self.href = ""

    def handle_data(self, data):
        if 0 <= data.find("第") and data.find("第") < data.find("回") and data.find("回") < data.find("本会議投票結果"):
            key = unicode(data, "utf8")
            key = utils.numzentohan(key)
            key = utils.erasewhitespace(key)
            key = key[key.find(u"第")+1:key.find(u"回")]
            self.sess = Session.get_by_key_name(key)
