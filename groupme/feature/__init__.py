#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from dataclasses import dataclass
from typing import Tuple

Level = str
Text = str
Title = Tuple[Level, Text]

HEADLINE = (r'^(?P<level>([\d|I|a|b|c]+\.?)+)'
            r'[ ]+'
            r'(?P<title>[\w]+[\w| |\d|\.|&|:]+)$')


@dataclass
class RawSection:
    """Section with title(level,title) and content(text)"""
    title: str = ''
    text: str = ''
    level: str = None


def create_raw(headline: Tuple[str, str], text) -> RawSection:
    raw = RawSection()
    if text:
        raw.text = ''.join(text)
    if headline:
        raw.title = headline[1]
        raw.level = headline[0]
    return raw


def format_title(title: Title) -> str:
    """Convert title to str"""
    return '%s %s' % (title[0], title[1])
