# -*- coding: utf-8 -*-

"""
Scenario Direction Extension for Python-Markdown
==================================

License: [GPLv3](https://opensource.org/licenses/GPL-3.0)
"""

from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re


class ScenarioDirectionExtension(Extension):
    """ Add scenario direction to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of ScenarioDirectionProcessor to BlockParser. """
        md.parser.blockprocessors.add('scenario_direction', 
                                      ScenarioDirectionProcessor(md.parser),
                                      '<paragraph')


class ScenarioDirectionProcessor(BlockProcessor):
    """ Process Scenario Direction. """

    RE = re.compile(r"(^|\n)※(.+?)(\n|$)")
    BGIMG_RE = re.compile(r"背景[:：]([^:：]+)(?:[:：](.+))?")

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            before = block[:m.start()] # All lines before direction
            after = block[m.end():]    # All lines after direction
            if before:
                # As the direction was not the first line of the block and the
                # lines before the direction must be parsed first,
                # recursively parse this lines as a block.
                self.parser.parseBlocks(parent, [before])
            # Create direction
            body = m.group(2)
            # background-image
            m = self.BGIMG_RE.match(body)
            if m:
                img = etree.SubElement(parent, 'img')
                img.attrib['class'] = 'background'
                img.attrib['src'] = m.group(1)
                if m.group(2):
                    img.attrib['alt'] = m.group(2)
                else:
                    img.attrib['alt'] = ''
            # TODO: other direction
            if not m:
                p = etree.SubElement(parent, 'p')
                p.attrib['class'] = 'comment'
                p.text = body
            if after:
                # Insert remaining lines as first block for future parsing.
                blocks.insert(0, after)
        else:
            # This should never happen, but just in case...
            logger.warn("We've got a problem header: %r" % block)


def makeExtension(*args, **kwargs):
    return ScenarioDirectionExtension(*args, **kwargs)
