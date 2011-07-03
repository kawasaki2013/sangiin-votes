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
import logging
import re
import utils
from google.appengine.ext import db
from VoteItem import VoteItem

class Session(db.Model):
    name = db.StringProperty(required=True)
    start = db.DateProperty(required=False)
    end = db.DateProperty(required=False)
    sort = db.StringProperty(required=False)
    itemcount = db.IntegerProperty(required=True)

set_sess_r = re.compile(u"[^0-9]+([0-9]+)[^0-9]+", re.UNICODE)

def setsession(name):
    sess = None
    name = utils.numzentohan(name)
    name = name.replace(u"　", u"")
    name = name.replace(u" ", u"")
    name = name.replace(u"\n", u"")
    name = name.replace(u"\r", u"")
    m = set_sess_r.search(name)
    if m != None and m.lastindex == 1:
        key  = m.string[m.start(1):m.end(1)]
        sess = Session.get_by_key_name(key)
        if sess == None:
            sess = Session(key_name=key, name=name, itemcount=0)
            db.put(sess)
            logging.info("Session:" + sess.key().name() + " " + sess.name)
    return sess

def getitemcount(sess):
    q = VoteItem.all()
    q.ancestor(sess)
    return q.count()

def updatesessionitemcount():
    for sess in Session.all():
        count = getitemcount(sess)
        if sess.itemcount != count:
            sess.itemcount = count
            sess.put()
            logging.info(sess.name + ":" + str(sess.itemcount))
