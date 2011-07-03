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
from google.appengine.ext import db

class Parameter(db.Model):
    desc = db.StringProperty(required=True)
    value = db.StringProperty(required=True)

def initparameter(params):
    for param in params:
        item = Parameter.get_by_key_name(param["name"])
        if item == None:
            item = Parameter(key_name=param["name"], desc=param["desc"], value=str(param["value"]))
            item.put()

def getparameter(key):
    param = Parameter.get_by_key_name(key)
    if param == None:
        return None
    else:
        return param.value
