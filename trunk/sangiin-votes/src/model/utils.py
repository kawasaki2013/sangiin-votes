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

def numzentohan(text):
    text = text.replace(u"０", u"0")
    text = text.replace(u"１", u"1")
    text = text.replace(u"２", u"2")
    text = text.replace(u"３", u"3")
    text = text.replace(u"４", u"4")
    text = text.replace(u"５", u"5")
    text = text.replace(u"６", u"6")
    text = text.replace(u"７", u"7")
    text = text.replace(u"８", u"8")
    text = text.replace(u"９", u"9")
    return text

def erasewhitespace(text):
    text = text.replace(u"　", u"")
    text = text.replace(u" ", u"")
    text = text.replace(u"\n", u"")
    text = text.replace(u"\r", u"")
    text = text.replace(u"\t", u"")
    return text
