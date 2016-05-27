# -*- coding: utf-8 -*-
"""
Scenario Paragraph Extension for Python-Markdown
==================================

License: [GPLv3](https://opensource.org/licenses/GPL-3.0)
"""

from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown import util
import re

NAME_RE = re.compile(r"^【([^】]+)】(.*)")
COMMENT_RE = re.compile(r"^※(.*)$")

class ScenarioParagraphTreeprocessor(Treeprocessor):
    def run(self, doc):
        for elem in doc.getiterator():
            if elem.tag != "p":
                continue
            if not elem.text:
                if len(elem) == 1 and elem[0].tag == "img":
                    elem.set("class", "image")
                continue
            m = NAME_RE.match(elem.text)
            if m:
                elem.text = None
                span = util.etree.Element("span")
                span.text = m.group(1)
                span.tail = m.group(2)
                span.set("class", "name")
                elem.insert(0, span)
                cls_type = "speech"
            elif COMMENT_RE.match(elem.text):
                elem.text = elem.text[1:]
                cls_type = "comment"
            else:
                cls_type = "description"
            cls = elem.get("class")
            if cls:
                elem.set("class", "{} {}".format(cls, cls_type))
            else:
                elem.set("class", cls_type)
            if elem.tail and elem.tail.strip():
                span = util.etree.Element("span")
                span.text = elem.tail
                span.set("class", "tail")
                elem.tail = None
                elem.insert(len(elem), span)


class ScenarioParagraphExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add(
            'scenario_paragraph',
            ScenarioParagraphTreeprocessor(md),
            '>prettify'
        )

def makeExtension(*args, **kwargs):
    return ScenarioParagraphExtension(*args, **kwargs)
