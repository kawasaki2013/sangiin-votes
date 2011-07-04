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
import cgi
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from model.Session import Session
from model.VoteSessionParty import VoteSessionParty

class SessItem:
    def __init__(self, seq, name, start, end, itemcount):
        self.seq = seq
        self.name = name
        self.beg = start
        self.end = end
        self.itemcount = itemcount
    seq = ""
    name = ""
    beg = None
    end = None
    itemcount = 0

class PartyItem:
    def __init__(self, name, aye, nay, rate):
        self.name = name
        self.aye = aye
        self.nay = nay
        self.rate = rate
    name = ""
    aye = 0
    nay = 0
    rate = 0.0

class MainPage(webapp.RequestHandler):

    def get(self):
        sesskey = cgi.escape(self.request.get('sess'))
        sess = Session.get_by_key_name(sesskey)
        sessitem = SessItem(sess.key().name(), sess.name, sess.start, sess.end, sess.itemcount)
        q = VoteSessionParty.all()
        q.ancestor(sess)
        items = []
        for party in q:
            items.append(PartyItem(party.key().name(), party.aye, party.nay, party.rate))
        template_values = { "sess":sessitem, "items":items }
        path = os.path.join(os.path.dirname(__file__), 'template/listsessparty.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/list/sessparty', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
