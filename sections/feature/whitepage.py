# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Concept
=======

use footer and header to detect white pages

3 types of white pages:

    - complete white: blank page
    - white page with footer and or header
    - content: that's not a whitepage

required resources:

    - text
    - position
    - footer

"""

import collections
import enum
import typing

import iamraw
import serializeraw
import texmex
import utila

PageContentWhitepages = collections.namedtuple(
    'PageContentWhitepages',
    'content, page',
)


class WhitePage(enum.Enum):
    CONTENT = -1
    BLANK = 0  # nothing on the page
    WHITE = 1  # page with footer and/or header


def work(
        document: str,
        position: str,
        footers: str,
        pages=None,
) -> str:
    """Extract `WhitePage` out of document.

    There are three types of `Whitepage`: BLANK, WHITE AND CONTENT

    Args:
        document(path): path to document text
        position(path): path to document text positions
        footers(path): path to extract footers
        pages(list): select `pages` to load
    Returns:
        dumped `yaml` result of extracted whitepages
    """
    # convert to make pages serializeable
    pages = tuple(pages) if pages else None

    # load
    document = serializeraw.load_document(document, pages=pages)
    position = serializeraw.load_textpositions(position, pages=pages)

    headerfooters = serializeraw.load_headerfooter(
        footers,
        pages=pages,
    )

    navigators = texmex.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    # work
    extracted = extract_whitepages(
        document,
        navigators,
        headerfooters,
    )
    dumped = serializeraw.dump_whitepages(extracted)
    return dumped


def extract_whitepages(
        document: iamraw.Document,
        navigators: typing.List[texmex.PageTextNavigator],
        headerfooters,
):
    result = {}
    for pagenumber, (currentpage, navigator, headerfooter) in utila.sync_pages([
            document,
            navigators,
            headerfooters,
    ]):
        header, footer = None, None
        if headerfooter:
            header, footer = headerfooter.header, headerfooter.footer

        if not navigator:
            result[pagenumber] = WhitePage.BLANK
            continue

        if not header and not footer:
            if not currentpage.children:
                result[pagenumber] = WhitePage.BLANK
            else:
                # Elements on the page, maybe title page, chapter page...
                result[pagenumber] = WhitePage.CONTENT
        else:
            top = header.end if header else texmex.START
            bottom = footer.begin if footer else texmex.END
            if not navigator.between(top, bottom):
                result[pagenumber] = WhitePage.WHITE
            else:
                # page with footer and/or header and content - "normal page"
                result[pagenumber] = WhitePage.CONTENT

    result = [
        PageContentWhitepages(
            page=page,
            content=WhitePage[whitepage.name] if whitepage else None,
        ) for page, whitepage in result.items()
    ]
    result = sorted(result, key=lambda x: x.page)
    return result


def whitepage_value_to_percent(whitepage: WhitePage):
    if whitepage is None or whitepage == '':
        # TODO: str comparison is not very consequent, but ok in the moment
        return 0.0
    return 1.0
