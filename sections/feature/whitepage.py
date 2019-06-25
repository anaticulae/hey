# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Concept:
    use footer and header to detect white pages

    2 types of white pages:
        - complete white: blank page
        - white page with footer and or header

    Required resources:
        text
        position
        footer
"""

from enum import Enum
from typing import List

from iamraw import Document
from serializeraw import load_document
from serializeraw import load_horizontals
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load

from groupme.feature.footer import extract_pages
from groupme.feature.numbers import load_textposition
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import create_pagetextnavigator
from hey.textnavigator.navigator import percent_from_pagesize


class WhitePage(Enum):
    BLANK = 0  # nothing on the page
    WHITE = 1  # page with footer and/or header


def work(document: str, position: str, horizontal_lines: str) -> str:
    # load
    document = load_document(document)
    position = load_textposition(position)
    horizontals = load_horizontals(horizontal_lines)

    # TODO: Think about how to handle this, invocation order of features?
    headerfooters = extract_pages(horizontals)
    navigators = create_pagetextnavigator(position, document)

    # work
    extracted = extract_whitepages(document, navigators, headerfooters)
    dumped = dump_whitepages(extracted)
    return dumped


def extract_whitepages(
        document: Document,
        navigators: List[PageTextNavigator],
        headerfooters,
):
    result = []
    for page, navigator, headerfooter in zip(
            document,
            navigators,
            headerfooters,
    ):
        header, footer = headerfooter
        height = navigator.height

        if not header and not footer:
            if page.children:
                # Elements on the page, maybe title page, chapter page...
                result.append(None)
            else:
                result.append(WhitePage.BLANK)
        else:
            top = percent_from_pagesize(height, header) if header else 0.0
            bottom = percent_from_pagesize(height, footer) if footer else 1.0
            if not navigator.between(top, bottom):
                result.append(WhitePage.WHITE)
            else:
                # page with footer and/or header and content - "normal page"
                result.append(None)
    return result


def whitepage_value_to_percent(whitepage: WhitePage):
    if whitepage is None or whitepage == '':
        # TODO: str comparison is not very consequent, but ok in the moment
        return 0.0
    return 1.0


def dump_whitepages(pages) -> str:
    result = []
    for index, whitepage in enumerate(pages):
        result.append({
            'page': index,
            'whitepage': whitepage.name if whitepage else '',
        })
    return dump(result)


def load_whitepages(content: str) -> List[WhitePage]:
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    result = []
    for item in loaded:
        whitepage = item['whitepage']
        if not whitepage:
            result.append(None)
        else:
            result.append(WhitePage[whitepage])
    return result
