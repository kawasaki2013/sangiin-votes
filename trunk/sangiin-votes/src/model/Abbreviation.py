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
from Session import Session
from VoteItem import VoteItem
from VoteItemParty import VoteItemParty
from AbbreviationGuide import AbbreviationGuide
from google.appengine.ext import db

class Abbreviation(db.Model):
    name = db.StringProperty(required=False)

def getabrvdict():
    dict = {}
    for abrv in Abbreviation.all():
        dict[abrv.key().name()] = abrv.name
    return dict

def abrvgetguide(key):
    name = None
    for guide in AbbreviationGuide.all():
        if key.startswith(guide.key().name()):
            name = guide.name
            break
    return name

def abrvapplyguide():
    for abrv in Abbreviation.all():
        if abrv.name == None or abrv.name == "":
            name = abrvgetguide(abrv.key().name())
            if name != None:
                abrv.name = name
                abrv.put()
                logging.info("Abbreviation:" + abrv.key().name() +" <-- " + abrv.name)

def abrvupdate():
    for sess in Session.all():
        q1 = VoteItem.all()
        q1.ancestor(sess)
        for item in q1:
            q2 = VoteItemParty.all()
            q2.ancestor(item)
            for party in q2:
                abrv = Abbreviation.get_by_key_name(key_names=party.key().name())
                if abrv == None:
                    abrv = Abbreviation(key_name=party.key().name(), name="")
                    abrv.put()
                    logging.info("Abbreviation:" + abrv.key().name())
    abrvapplyguide()
