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

import serializeraw
from iamraw import Document
from utila import NEWLINE
from utila import Flag
from utila import call
from utila import debug
from utila import error

from groupme.feature import format_title
from groupme.feature.toc import toc
from groupme.structure import body


def work(documentpath: str) -> str:
    document = serializeraw.load_document(documentpath)

    result = chapters(document)
    dumped = serializeraw.dump_chapter(result)
    return dumped


def chapters(document: Document):
    """Extract chapter structure from document path"""
    call('chapter')
    tableofcontent = toc(document)
    if not tableofcontent:
        # this appraoch does not work without headlines, we can not split by
        # headline if there are no headlines.
        return []
    content = body(document)
    result = []

    def log_error(headline):
        error('can not split chapter')
        error(headline)
        error('empty chapter')

    for title in tableofcontent[1:]:  # skip the first one
        print(title)
        debug('process `%s`' % str(title))
        _level, _title = title.level, title.title
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
            log_error(headline)
            continue
        _title, _content = current_chapter.split(NEWLINE, maxsplit=1)
        result.append({
            'level': _level,
            'title': _title,
            'content': _content,
        })

    if not content:
        # TODO: investigate here to check that no content is lost
        log_error('last headline')
        return result
    _title, _content = content.split(NEWLINE, maxsplit=1)
    _level, _title = _title.split(maxsplit=1)
    result.append({
        'level': _level,
        'title': _title,
        'content': _content,
    })
    return result


def name():
    return 'chapter'


def commandline():
    return Flag(
        longcut=name(),
        message='extract chapter with title and content',
    )
