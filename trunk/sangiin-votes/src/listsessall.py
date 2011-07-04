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
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from model.Session import Session

class SessItem:
    def __init__(self, seq, name, start, end):
        self.seq = seq
        self.name = name
        self.beg = start
        self.end = end
    seq = ""
    name = ""
    beg = None
    end = None

class MainPage(webapp.RequestHandler):

    def get(self):
        items = []
        for sess in Session.all():
            if 0 < sess.itemcount:
                items.append(SessItem(sess.key().name(), sess.name, sess.start, sess.end))
        items.reverse()
        template_values = { "items":items }
        path = os.path.join(os.path.dirname(__file__), 'template/listsessall.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/list/sessall', MainPage), ('/', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
