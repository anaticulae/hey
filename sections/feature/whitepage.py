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

from collections import namedtuple
from enum import Enum
from functools import lru_cache
from typing import List

from iamraw import Document
from serializeraw import load_document
from serializeraw import load_horizontals
from utila import INF
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load

from groupme.feature.footer import extract_pages
from groupme.feature.numbers import load_textposition
from hey import CACHE_SMALL
from hey.textnavigator.navigator import END
from hey.textnavigator.navigator import START
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import create_pagetextnavigators
from hey.textnavigator.navigator import percent_from_pagesize
from hey.utils import sync

PageContentWhitepages = namedtuple('PageContentWhitepages', 'content, page')


class WhitePage(Enum):
    CONTENT = -1
    BLANK = 0  # nothing on the page
    WHITE = 1  # page with footer and/or header


def work(document: str, position: str, horizontals: str, pages=None) -> str:
    # load
    pages = tuple(pages) if pages else None
    document = load_document(document, pages=pages)
    position = load_textposition(position, pages=pages)
    horizontals = load_horizontals(horizontals, pages=pages)

    # TODO: Think about how to handle this, invocation order of features?
    headerfooters = extract_pages(horizontals)
    navigators = create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    # work
    extracted = extract_whitepages(
        document,
        navigators,
        headerfooters,
    )
    dumped = dump_whitepages(extracted)
    return dumped


def extract_whitepages(
        document: Document,
        navigators: List[PageTextNavigator],
        headerfooters,
):
    """
    Args:
        headerfooters:
            Position
    """
    result = {}
    navigators = sorted(navigators.values(), key=lambda x: x.page)
    for pagenumber, (currentpage, navigator, headerfooter) in sync([
            document,
            navigators,
            headerfooters,
    ]):
        header, footer = headerfooter.content if headerfooter else (None, None)
        if not navigator:
            result[pagenumber] = WhitePage.BLANK
            continue
        height = navigator.height
        if not header and not footer:
            if not currentpage.children:
                result[pagenumber] = WhitePage.BLANK
            else:
                # Elements on the page, maybe title page, chapter page...
                result[pagenumber] = WhitePage.CONTENT
                # result[pagenumber] = None
        else:
            top = percent_from_pagesize(height, header) if header else START
            bottom = percent_from_pagesize(height, footer) if footer else END
            if not navigator.between(top, bottom):
                result[pagenumber] = WhitePage.WHITE
            else:
                # page with footer and/or header and content - "normal page"
                result[pagenumber] = WhitePage.CONTENT

    result = {
        page: PageContentWhitepages(
            page=page,
            content=WhitePage[whitepage.name] if whitepage else None,
        ) for page, whitepage in result.items()
    }
    return result


def whitepage_value_to_percent(whitepage: WhitePage):
    if whitepage is None or whitepage == '':
        # TODO: str comparison is not very consequent, but ok in the moment
        return 0.0
    return 1.0


def dump_whitepages(pages) -> str:
    """Dump list of dict"""
    result = {}
    if isinstance(pages, list):
        pages = {item.page: item for item in pages}
    for page, value in pages.items():
        result[page] = value.content.name if value.content else None
    return dump(result)


@lru_cache(CACHE_SMALL)
def load_whitepages(content: str) -> List[WhitePage]:
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)
    result = [
        PageContentWhitepages(
            page=page,
            content=WhitePage[whitepage] if whitepage else None,
        ) for page, whitepage in loaded.items()
    ]
    return result
