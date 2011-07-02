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
import logging
import re
import utils
from google.appengine.ext import db

class Nengo(db.Model):
    first = db.IntegerProperty(required=True)

set_nengo_r = re.compile(u"([^0-9]+)([0-9]+)年[^0-9]*([0-9]+)年", re.UNICODE)
wareki_text_r = re.compile(u"([^0-9]+)([0-9]+)[^0-9]*年([0-9]+)[^0-9]*月([0-9]+)[^0-9]*日", re.UNICODE)
warekiex_text_r = re.compile(u"([^0-9]+)([0-9]+)[^0-9]*年（[0-9]+年）([0-9]+)[^0-9]*月([0-9]+)[^0-9]*日", re.UNICODE)

def setnengo(nengo_year_text):
    nengo_year_text = utils.numzentohan(nengo_year_text)
    nengo_year_text = utils.erasewhitespace(nengo_year_text)
    nengo_year_text = nengo_year_text.replace(u"（", u"")
    nengo_year_text = nengo_year_text.replace(u"）", u"")
    m = set_nengo_r.search(nengo_year_text)
    if m != None and m.lastindex == 3:
        name  = m.string[m.start(1):m.end(1)]
        wanen = int(m.string[m.start(2):m.end(2)])
        year  = int(m.string[m.start(3):m.end(3)])
        first = year - wanen + 1
        nengo = Nengo.get_by_key_name(name)
        if nengo == None:
            nengo = Nengo(key_name=name, first=first)
            db.put(nengo)
            logging.info("Nengo:" + nengo.key().name() + str(nengo.first))

def getdatefromwareki(wareki_text):
    wareki_text = utils.numzentohan(wareki_text)
    wareki_text = utils.erasewhitespace(wareki_text)
    if 0 < wareki_text.find(u"（"):
        m = warekiex_text_r.search(wareki_text)
    else:
        m = wareki_text_r.search(wareki_text)
    if m != None and m.lastindex == 4:
        name  = m.string[m.start(1):m.end(1)]
        wanen = int(m.string[m.start(2):m.end(2)])
        mon = int(m.string[m.start(3):m.end(3)])
        day = int(m.string[m.start(4):m.end(4)])
        nengo = Nengo.get_by_key_name(name)
        return datetime.date(nengo.first + wanen -1, mon, day)
    else:
        return None
