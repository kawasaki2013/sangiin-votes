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
#import datetime
#import logging
import os
#import re
import yaml
#from google.appengine.api import taskqueue
#from google.appengine.ext import db
from parser.IndexParser import IndexParser
from parser.SessionParser import SessionParser
from parser.VoteParser import VoteParser
import model.Abbreviation

def main():

    conf = yaml.load(file(os.path.join(os.path.dirname(__file__), 'conf.yaml'), 'r'))
    indexParser = IndexParser()
    indexParser.parse(conf['index_url'])
    for sess in indexParser.links:
        sessionParser = SessionParser()
        sessionParser.parse(sess)
        for vote in sessionParser.links:
            voteParser = VoteParser(sessionParser.sess)
            voteParser.parse(vote)
    model.Abbreviation.generate()

    print 'Content-Type: text/plain'
    print ''
    print 'OK'

if __name__ == "__main__":
    main()
