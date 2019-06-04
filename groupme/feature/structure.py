# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from re import match

from iamraw import Document
from iamraw import Page

from groupme.feature import HEADLINE
from groupme.feature import create_raw
from groupme.feature import format_title


def header(document: Document) -> str:
    from groupme.feature.toc import toc
    tableofcontent = toc(document)
    # Split content from header due first headline
    first_headline = format_title(tableofcontent[0])
    splitted = document.text.rsplit(first_headline, 1)
    assert len(splitted[0]) > 300  # front page, toc etc.
    return splitted[0]


def body(document: Document) -> str:
    header_ = header(document)
    result = document.text.split(header_)[1]
    return result


def sections(document: Document):
    """Determine `sections` from `Document`"""
    result = []
    for page in document.pages:
        result.extend(sections_from_page(page))
    return result


def sections_from_page(page: Page):
    result, headline, text = [], None, []
    for line in page.text.splitlines():
        parsed = parse_headline(line)
        if parsed:
            if text or headline:
                result.append(create_raw(headline, text))
            headline = parsed
            text = []
        else:
            text.append(line)
    if text:
        result.append(create_raw(headline, text))
    return result


def parse_headline(line: str):
    assert isinstance(line, str)
    matched = match(HEADLINE, line)
    if not matched:
        return None
    level = matched['level']
    if len(level) <= 2 and level[0].islower():
        return None
    return (level, matched['title'])
