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
from htmllib import HTMLParser
from formatter import NullFormatter
from google.appengine.api import urlfetch

class BaseParser(HTMLParser):

    base = ""
    href = ""
    
    def __init__(self):
        HTMLParser.__init__(self, NullFormatter())
        
    def parse(self, url):
        self.base = ""
        self.href = ""
        m = re.compile(".*/").match(url)
        if m != None:
            self.base = m.string[m.start(0):m.end(0)]
        result = urlfetch.fetch(url, headers = {'Cache-Control' : 'max-age=30', 'Pragma' : 'no-cache'} )
        if result.status_code == 200:
            logging.debug(str(result.status_code) + " OK " + url)
            HTMLParser.feed(self, result.content)
            HTMLParser.close(self)
        else:
            logging.error(str(result.status_code) + " NG " + url)
