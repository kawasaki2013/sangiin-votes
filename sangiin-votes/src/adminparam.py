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
from model.Parameter import Parameter

class AdminParamItem:
    name = ""
    desc = ""
    value = ""
    def __init__(self, name, desc, value):
        self.name = name
        self.desc = desc
        self.value = value

class AdminParam(webapp.RequestHandler):

    def post(self):
        name = cgi.escape(self.request.get('name'))
        value = cgi.escape(self.request.get('value'))
        if self.request.get('add') != "":
            if value != "" and name != "":
                item = Parameter.get_by_key_name(name)
                if item != None and item.value != value:
                    item.value = value
                    item.put()
        self.redirect('/admin/param', permanent=False)

    def get(self):
        items = []
        for param in Parameter.all():
            items.append(AdminParamItem(param.key().name(), param.desc, param.value))
        template_values = { "items": items }
        path = os.path.join(os.path.dirname(__file__), 'template/adminparam.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/admin/param', AdminParam)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
