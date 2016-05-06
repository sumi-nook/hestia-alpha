# -*- coding: utf-8 -*-
"""
Text span Extension for Python-Markdown
==================================

License: [GPLv3](https://opensource.org/licenses/GPL-3.0)
"""

from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown import util

class TextSpanTreeprocessor(Treeprocessor):
    def run(self, doc):
        for elem in doc.getiterator():
            if elem.tag != "p":
                continue
            if elem.text and elem.text.strip():
                span = self.create_span()
                span.text = elem.text
                elem.text = None
                elem.insert(0, span)
            for i, child in enumerate(elem):
                if child.tail and child.tail.strip():
                    span = self.create_span()
                    span.text = child.tail
                    child.tail = None
                    elem.insert(i+1, span)

    def create_span(self):
        span = util.etree.Element("span")
        span.set("class", "text")
        return span


class TextSpanExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add(
            'text_span',
            TextSpanTreeprocessor(md),
            '>prettify'
        )

def makeExtension(*args, **kwargs):
    return TextSpanExtension(*args, **kwargs)
