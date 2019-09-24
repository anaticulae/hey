# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Example driven programming:

for chapter in document:
    for headline in chapter:
        p(headline)

Required resources:
    sections
    text
    font?


TODO: New concept:

Collect all title, cluster them by size and font distance and derivate the
headline level out of these information. Use further text information out of
headline.
"""

import typing

import iamraw
import utila
from iamraw import Border
from iamraw import Headline
from iamraw import PagesHeadlineList
from serializeraw import dump_headlines
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_pageborders
from serializeraw import load_sections

from groupme.feature.footer import document_footerheader
from groupme.feature.footer import footerborder_to_border
from groupme.feature.numbers import load_textposition
from hey.document import BorderList
from hey.document import document_border
from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from hey.textnavigator.fonts import document_textsize
from hey.textnavigator.fonts import fontdistance_textbounds
from hey.textnavigator.fonts import fontsize_from_textbounds
from hey.textnavigator.fonts import textbounds
from hey.textnavigator.navigator import PageTextContentNavigator
from hey.textnavigator.navigator import PageTextNavigators
from hey.textnavigator.navigator import create_pagetextnavigators
from hey.textnavigator.navigator import navigator_to_bounds
from sections.feature.sections import Content
from sections.feature.sections import Sections
from sections.feature.sections import chapters


@utila.checkdatatype
def work(
        sections: str,
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        sizeandborder: str,
        horizontals: str,
) -> str:
    """Extract headlines out of data

    Args:
        sections
        text
        text_position
        font_header
        sizeandborder
        horizontals
    """
    # prepare
    document = load_document(text)
    position = load_textposition(text_position)
    sections = load_sections(sections)
    sizeandborder = load_pageborders(sizeandborder)
    horizontals = load_horizontals(horizontals)

    pagetextnavigators = create_pagetextnavigators(
        text=document,
        text_positions=position,
    )
    fontstore = create_fontstore(
        font_header,
        font_content,
    )
    # work
    extracted = extract_headlines(
        sections,
        pagetextnavigators=pagetextnavigators,
        fontstore=fontstore,
        sizeandborder=sizeandborder,
        horizontals=horizontals,
        chapter=None,
    )

    # save
    dumped = dump_headlines(extracted)
    return dumped


SMALLEST_HEADLINE_FACTOR = 1.1  # TODO: HOLY VALUE
FIRST_LEVEL = 0.9  # TODO: HOLY VALUE
SECOND_LEVEL = 0.7


def extract_headlines(
        sections: Sections,
        pagetextnavigators: PageTextNavigators,
        fontstore: FontStore,
        sizeandborder,
        horizontals,
        chapter: int = 0,
):
    assert isinstance(sections, Sections), type(sections)
    assert sections, 'no sections provided'
    if chapter is None:
        # TODO: clearify code
        # analyze all chapter of the document
        chapter = sum([
            len(item.content) for item in sections if isinstance(item, Content)
        ])
        chapter = list(range(0, chapter))
    content = chapters(sections)
    chapter = [chapter] if isinstance(chapter, int) else chapter

    contentborders = [item.border for item in sizeandborder]
    border = content_border(horizontals, contentborders)

    textsize = document_textsize(
        navigators=pagetextnavigators,
        borders=sizeandborder,
    )
    smallest_headline_size = textsize * SMALLEST_HEADLINE_FACTOR

    result = []
    for index in chapter:
        chaptercontent = []
        (start, end) = content[index]
        for page in range(start, end + 1):
            pagecontent = PageTextContentNavigator(
                utila.select_page(pagetextnavigators, pagenumber=page),
                border,
            )
            xoff = pagecontent.offset[0]
            xoff = xoff if xoff is not None else 0
            bounds = navigator_to_bounds(pagecontent)
            bounds = textbounds(pagecontent, border)
            without_content = [item[0] for item in bounds]
            # PageContentNavigator, the header and footer is ignored
            distances = fontdistance_textbounds(without_content)
            for containerid, (item, text) in enumerate(bounds, start=xoff):
                distanceid = containerid - xoff
                # font = fontstore.font(page, containerid, line=0, char=0)
                splitted = text.splitlines()
                if len(splitted) > 1:
                    continue
                fontsize = fontsize_from_textbounds(item)
                if fontsize <= smallest_headline_size:
                    # text is to small to be a headline
                    continue
                try:
                    level = distances[distanceid] + distances[distanceid + 1]
                except IndexError:
                    level = distances[distanceid] * 2
                headline = Headline(
                    container=containerid,
                    level=level,
                    page=page,
                    text=text,
                )
                chaptercontent.append(headline)
        result.append(chaptercontent)

    convert_level(result)
    return result


HORIZONTAL_MIN_COUNT = 5  # TODO: HOLY VALUES


def content_border(
        horizontals: typing.List[iamraw.HorizontalLine],
        contentborders: BorderList,
) -> Border:
    """Determine the content border as a result of left/right-side and detected
    footer.

    If no `horizontals` are provied, the `contentborders` is the only
    source of detecting the border.

    If `horizontals` are provided the horizontals determine top and
    bottom border. The content defines the border left and right.

    TODO: What should we do, if only top or only bottom horizontal line
    are provided?

    Args:
        horizontals:
        contentborders:
    Return:
        single `Border` which separates the textual content from footer
        and header with text and pagecount.
    """

    leftright = document_border(contentborders)

    if not horizontals:
        return leftright

    # Using one or two horizontals for determining the footer or header
    # makes no sence. Therefore we need some elements.
    if len(horizontals) < HORIZONTAL_MIN_COUNT:
        return leftright

    border = document_footerheader(horizontals)
    border = footerborder_to_border(border)
    assert border.bottom > 0, str(border)

    result = Border(
        bottom=border.bottom,
        left=leftright.left,
        right=leftright.right,
        top=border.top,
    )
    return result


def convert_level(result: PagesHeadlineList) -> int:
    """Convert chapter level based on text distances to logical level
    (1,2,3,4,...).

    Hint: This function updates the level
    TODO: copy items
    """

    # pylint:disable=len-as-condition
    utila.call('convert_level')
    utila.info('empty PageHeadlineList')
    if not result:
        return result

    if not any(result):
        return []

    maxsize = max([
        max([item.level for item in chapter]) for chapter in result if chapter
    ])
    first_level = FIRST_LEVEL * maxsize
    second_level = SECOND_LEVEL * maxsize

    def get_level(value):
        if value >= first_level:
            return 1
        if value >= second_level:
            return 2
        return 3

    # TODO: copy elements
    for items in result:
        for item in items:
            item.level = get_level(item.level)
    return result
