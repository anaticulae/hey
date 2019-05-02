#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""How to extract text blocks out of the text and chapter structure

    1. Split the whole content by headlines into seprate blocks
        1.a. Skip non text blocks
    2.

"""

from iamraw import Document
from utila import NEWLINE
from yaml import dump

from groupme.feature import format_title
from groupme.feature.structure import body
from groupme.feature.toc import toc


def chapters(document: Document):
    """Extract chapter structure from document path"""
    tableofcontent = toc(document)
    content = body(document)
    result = []
    for title in tableofcontent[1:]:  # skip first one
        headline = format_title(title)
        current_chapter, headline, rest = content.partition(headline)
        content = headline + rest
        result.append(current_chapter)
    result.append(content)
    return result


def chapter_to_yaml(chapter):
    result = []
    for item in chapter:
        title, _, content = item.partition(NEWLINE)
        result.append({'title': title, 'content': content})
    return dump(result)
