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

from functools import lru_cache
from typing import Dict
from typing import List

from iamraw import Document
from serializeraw import load_document
from utila import NEWLINE
from utila import Flag
from utila import call
from utila import debug
from utila import error
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load

from groupme.feature import format_title
from groupme.feature.toc import toc
from groupme.structure import body
from hey import CACHE_SMALL


def work(documentpath: str) -> str:
    document = load_document(documentpath)

    result = chapters(document)
    dumped = dump_chapter(result)
    return dumped


def chapters(document: Document):
    """Extract chapter structure from document path"""
    call('chapter')
    tableofcontent = toc(document)
    content = body(document)
    result = []
    for title in tableofcontent[1:]:  # skip first one
        debug('process `%s`' % str(title))
        _level, _title = title
        headline = format_title(title)
        current_chapter, headline, rest = content.partition(headline)
        if not headline:
            # split with chapter level was not successfull, try without level
            simple_splitter = _title + NEWLINE
            current_chapter, headline, rest = content.partition(simple_splitter)

        content = headline + rest
        # TODO, WORKAROUND: there is a problem to split some chapter by
        # headlines. Improve this later.
        if not current_chapter:
            result.append({
                'level': _level,
                'title': _title,
                'content': '',
            })
            error('can not split chapter')
            error(headline)
            error('empty chapter')
            continue
        _title, _content = current_chapter.split(NEWLINE, maxsplit=1)
        result.append({
            'level': _level,
            'title': _title,
            'content': _content,
        })

    _title, _content = content.split(NEWLINE, maxsplit=1)
    _level, _title = _title.split(maxsplit=1)
    result.append({
        'level': _level,
        'title': _title,
        'content': _content,
    })
    return result


# TODO: Move to serialzeraw?
def dump_chapter(chapter: List[Dict]) -> str:
    result = []
    for item in chapter:
        level, title, content = item['level'], item['title'], item['content']
        result.append({
            'level': level,
            'title': title,
            'content': content,
        })
    dumped = dump(result)
    return dumped


@lru_cache(maxsize=CACHE_SMALL)
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
