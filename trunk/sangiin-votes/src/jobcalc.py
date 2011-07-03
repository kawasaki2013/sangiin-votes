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
from model.Parameter import getparameter
from model.Session import Session
from model.Session import updatesessionitemcount
from model.VoteItem import VoteItem
from model.VoteItemParty import VoteItemParty
from model.VoteSessionParty import VoteSessionParty
from model.Abbreviation import getabrvdict

def initsession(sess):
    logging.info("initsession(" + sess.key().name() + ")")
    q = VoteSessionParty.all()
    q.ancestor(sess)
    for votesess in q:
        votesess.total = sess.itemcount
        votesess.aye = 0
        votesess.nay = 0
        votesess.put()

def calcsession(sess, thrh, dict):
    logging.info("calcsession(" + sess.key().name() + ")")
    q1 = VoteItem.all()
    q1.ancestor(sess)
    votes = {}
    for item in q1:
        q2 = VoteItemParty.all()
        q2.ancestor(item)
        for voteitem in q2:
            if dict.has_key(voteitem.key().name()):
                abrv = dict[voteitem.key().name()]
                if votes.has_key(abrv):
                    votesess = votes[abrv]
                else:
                    votesess = VoteSessionParty.get_by_key_name(abrv, sess)
                    if votesess == None:
                        votesess = VoteSessionParty(parent=sess, key_name=abrv, total=sess.itemcount, aye=0, nay=0, rate=0.0)
                    votes[abrv] = votesess
                if thrh <= (voteitem.aye * 100 / voteitem.total):
                    votesess.aye = votesess.aye + 1
                if thrh <= (voteitem.nay * 100 / voteitem.total):
                    votesess.nay = votesess.nay + 1
            else:
                logging.error("No Abbreviation for " + voteitem.key().name())
    for key, votesess in votes.iteritems():
        votesess.rate = round(float(votesess.aye) / float(votesess.total) * 100, 1)
        votesess.put()
        logging.info(key + ":" + str(votesess.aye) + "/" + str(votesess.nay) + ":" + str(votesess.rate))

def main():
    sessbeg = int(getparameter("fetchbegsession"))
    sessend = int(getparameter("fetchendsession"))
    updatesessionitemcount()
    thrh = int(getparameter("partydecisionthreshold"))
    dict = getabrvdict()
    for sess in Session.all():
        sessno = int(sess.key().name())
        if 0 < sess.itemcount and sessbeg <= sessno and sessno <= sessend:
            initsession(sess)
            calcsession(sess, thrh, dict)
    print 'Content-Type: text/plain'
    print ''
    print 'OK'

if __name__ == "__main__":
    main()
