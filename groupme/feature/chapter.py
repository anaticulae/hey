#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""How to extract text blocks out of the text and chapter structure

    1. Split the whole content by headlines into seprate blocks
        1.a. Skip non text blocks
    2.

"""

from typing import Dict
from typing import List

from iamraw import Document
from serializeraw import load_document
from utila import NEWLINE
from utila import Flag
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load

from groupme.feature import format_title
from groupme.feature.toc import toc
from groupme.structure import body


def work(documentpath: str) -> str:
    document = load_document(documentpath)

    result = chapters(document)
    dumped = dump_chapter(result)
    return dumped


def chapters(document: Document):
    """Extract chapter structure from document path"""
    tableofcontent = toc(document)
    content = body(document)
    result = []
    for title in tableofcontent[1:]:  # skip first one
        headline = format_title(title)
        current_chapter, headline, rest = content.partition(headline)
        content = headline + rest

        _title, _content = current_chapter.split(NEWLINE, maxsplit=1)
        result.append({
            'title': _title,
            'content': _content,
        })

    _title, _content = content.split(NEWLINE, maxsplit=1)
    result.append({
        'title': _title,
        'content': _content,
    })
    return result


# TODO: Move to serialzeraw?
def dump_chapter(chapter) -> str:
    result = []
    for item in chapter:
        title, content = item['title'], item['content']
        result.append({
            'title': title,
            'content': content,
        })
    dumped = dump(result)
    return dumped


def load_chapter(content: str) -> List[Dict]:
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)
    return loaded


def name():
    return 'chapter'


def commandline():
    return Flag(
        longcut=name(),
        message='extract chapter with title and content',
    )
