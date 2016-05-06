# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import markdown

from extensions.ruby import RubyExtension
from extensions.scenario_paragraph import ScenarioParagraphExtension
from extensions.text_span import TextSpanExtension
from extensions.word_link import WordLinkExtension

def toXHTML(text):
    md = markdown.Markdown(extensions=[
        RubyExtension(),
        TextSpanExtension(),
        ScenarioParagraphExtension(),
        WordLinkExtension(),
    ])
    return """<div>
{}
</div>""".format(md.convert(text))
