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
from model.AbbreviationGuide import AbbreviationGuide

class AdminAbrvGuideItem:
    abrv = ""
    text = ""
    def __init__(self, abrv, text):
        self.abrv = abrv
        self.text = text

class AdminAbrvGuide(webapp.RequestHandler):

    def post(self):
        abrv = cgi.escape(self.request.get('abrv'))
        text = cgi.escape(self.request.get('text'))
        if self.request.get('add') != "":
            if abrv != "" and text != "":
                item = AbbreviationGuide.get_or_insert(text)
                if item.name != abrv:
                    item.name = abrv
                    item.put()
        elif self.request.get('del') != "":
            item = AbbreviationGuide.get_by_key_name(key_names=text)
            if item != None:
                item.delete()
        self.redirect('/admin/abrvguide', permanent=False)

    def get(self):
        items = []
        for guide in AbbreviationGuide.all():
            items.append(AdminAbrvGuideItem(guide.name, guide.key().name()))
        template_values = { "items": items }
        path = os.path.join(os.path.dirname(__file__), 'template/adminabrvguide.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/admin/abrvguide', AdminAbrvGuide)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
