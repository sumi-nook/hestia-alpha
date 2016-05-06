"""
Ruby Extension for Python-Markdown
==================================

Converts \[kana](-kanji) to <ruby><rb>kanji</rb><rp>(</rp><rt>kana</rt><rp>)</rp></ruby>.
Its syntax is same as http://pandoc.org/scripting.html#a-filter-for-ruby-text.

Arranged source: <https://github.com/mugwort-rc/mdx_ruby>
Original source: <https://github.com/mkszk/mdx_ruby>

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
"""

from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree
import re


class RubyExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        # append to inline patterns
        RUBY_RE = r'\[([^\]]+)\]\(ruby:([^\)]+)\)'
        md.inlinePatterns.add('ruby', Ruby(RUBY_RE), "<link")


class Ruby(Pattern):
    def handleMatch(self, m):
        kanji = m.group(2).strip()
        kana = m.group(3).strip()
        if kanji and kana:
            ruby = etree.Element('ruby')
            etree.SubElement(ruby, 'rb').text = kanji
            etree.SubElement(ruby, 'rp').text = '('
            etree.SubElement(ruby, 'rt').text = kana
            etree.SubElement(ruby, 'rp').text = ')'
        else:
            ruby = ''
        return ruby

def makeExtension(*args, **kwargs):
    return RubyExtension(*args, **kwargs)
