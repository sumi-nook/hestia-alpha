# -*- coding: utf-8 -*-
"""
Word link Extension for Python-Markdown
==================================

License: [GPLv3](https://opensource.org/licenses/GPL-3.0)
"""

from markdown.extensions import Extension
from markdown.inlinepatterns import AutolinkPattern

# for nenokami-kyouhime
# <word:専門用語>
WORDLINK_RE = r'<(?:word:)([^>]*)>'

class WordLinkExtension(Extension):
    """ Add word extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """ Modify inline patterns. """
        md.inlinePatterns.add(
            'wordlink',
            AutolinkPattern(WORDLINK_RE, md),
            '>autolink'
        )

