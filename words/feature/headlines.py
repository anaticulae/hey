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

TODO: DO NOT MIX STRATEGYS

TODO: New concept:

Collect all title, cluster them by size and font distance and derivate the
headline level out of these information. Use further text information out of
headline.
"""

import re
import typing
import warnings

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

import groupme.toc.regex
import hey.textnavigator.navigator
import sections.feature.sections
from groupme.feature.footer import document_footerheader
from groupme.feature.footer import footerborder_to_border
from groupme.feature.numbers import load_textposition
from hey.document import BorderList
from hey.document import document_border
from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from hey.textnavigator.fonts import document_textdistance
from hey.textnavigator.fonts import document_textsize
from hey.textnavigator.fonts import fontdistance_textbounds
from hey.textnavigator.fonts import fontsize_from_textbounds
from hey.textnavigator.fonts import textbounds
from hey.textnavigator.navigator import PageTextContentNavigator
from hey.textnavigator.navigator import PageTextNavigators
from hey.textnavigator.navigator import create_pagetextnavigators
from hey.textnavigator.navigator import navigator_to_bounds


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
        sections_=sections,
        pagetextnavigators=pagetextnavigators,
        fontstore=fontstore,
        sizeandborder=sizeandborder,
        horizontals=horizontals,
        chapters=None,
    )

    # TODO: We need the approach
    # More than one INDEPENDANT strategies
    # Execute them all
    # Run judge instance to select the best one
    dotted = isdotted(extracted)
    if dotted:
        extracted = filter_headlines(extracted)
    else:
        # TODO: EXTEND AND DOCUMENT THIS APPROACH
        # Rerun computation with differnet holy value
        extracted = extract_headlines(
            sections_=sections,
            pagetextnavigators=pagetextnavigators,
            fontstore=fontstore,
            sizeandborder=sizeandborder,
            horizontals=horizontals,
            chapters=None,
            smallest_headline_distance=SMALLEST_HEADLINE_DISTANCE_NOLEVEL,
        )

    # save
    dumped = dump_headlines(extracted)

    return dumped


WHITELIST = set([
    'Literaturverzeichnis',
    'Eidesstattliche Erklärung',
])


def filter_headlines(items: iamraw.PagesHeadlineList):
    dotted = isdotted(items)
    if dotted:
        result = []
        for chapter in items:
            chapter_headlines = []
            for headline in chapter:
                parsed = parse_headline(headline.text)
                if parsed:
                    chapter_headlines.append(headline)
                    continue
                if headline.text in WHITELIST:
                    chapter_headlines.append(headline)
                    continue
            result.append(chapter_headlines)
        return result

    warnings.warn('not dotted not supported')
    return items


MIN_DOTTED_COUNT = 0.1  # TODO: HOLY VALUE


def isdotted(items):
    assert items
    flat = utila.flatten(items)

    dotted = [item for item in flat if parse_headline(item.text)]
    percent = len(dotted) / len(flat)

    return percent >= MIN_DOTTED_COUNT


def parse_headline(line):
    line = line.strip()
    return re.match(HEADLINE, line) is not None


USER_CONTENT = r'\w\d\.&:, \-' + hey.utils.SPECIAL_MINUS_SIGN
# \W to ensure non-unicode character, like special - chars
HEADLINE = re.compile(
    (
        r'^'
        r'(?P<level>(\d{1,2}\.)+\d{0,2})'
        r'[ ]{1,5}'
        r'(?P<text>\w'  # ensure that text does not start with whitespace
        fr'[{USER_CONTENT}]+?)'
        r'$'),
    re.VERBOSE,
)

SMALLEST_HEADLINE_SIZE = 1.1  # TODO: HOLY VALUE
SMALLEST_HEADLINE_DISTANCE = 1.05  # TODO:HOLY VALUE
SMALLEST_HEADLINE_DISTANCE_NOLEVEL = 1.1  # TODO:HOLY VALUE
FIRST_LEVEL = 0.9  # TODO: HOLY VALUE
SECOND_LEVEL = 0.7


def extract_headlines(
        sections_: typing.List[sections.feature.sections.Sections],
        pagetextnavigators: PageTextNavigators,
        fontstore: FontStore,
        sizeandborder,
        horizontals,
        chapters: int = 0,
        smallest_headline_distance=SMALLEST_HEADLINE_DISTANCE,
) -> iamraw.PagesHeadlineList:
    """
    TODO: why do we need the chapter selector?
    """
    chapters, content = prepare_chapter_and_content(sections_, chapters)
    # bounding box of text content
    border = contentborder(sizeandborder, horizontals)

    textsize = document_textsize(
        navigators=pagetextnavigators,
        borders=sizeandborder,
    )
    textdistance = document_textdistance(
        navigators=pagetextnavigators,
        borders=sizeandborder,
    )

    smallest_headline_size = textsize * SMALLEST_HEADLINE_SIZE
    smallest_headline_distance = textdistance * smallest_headline_distance
    result = []
    for index in chapters:
        chaptercontent = extract_headlines_chapter(
            content[index],
            border,
            pagetextnavigators,
            smallest_headline_size,
            smallest_headline_distance,
        )
        result.append(chaptercontent)

    convert_level(result)
    return result


def extract_headlines_chapter(
        pagerange,
        border,
        pagetextnavigators,
        smallest_headlinesize,
        smallest_headlinedistance,
):
    result = []
    start, end = pagerange
    for page in range(start, end + 1):
        pagecontent = PageTextContentNavigator(
            utila.select_page(pagetextnavigators, pagenumber=page),
            border,
        )
        pageheadlines = extract_headlines_page(
            page,
            pagecontent,
            border,
            smallest_headlinesize,
            smallest_headlinedistance,
        )
        result.extend(pageheadlines)
    return result


def extract_headlines_page(
        page,
        pagecontent,
        border,
        smallest_headlinesize,
        smallest_headlinedistance,
):
    result = []
    xoff = pagecontent.offset[0]
    xoff = xoff if xoff is not None else 0
    bounds = navigator_to_bounds(pagecontent)
    bounds = textbounds(pagecontent, border)
    without_content = [item[0] for item in bounds]
    # PageContentNavigator, the header and footer is ignored
    distances = fontdistance_textbounds(without_content)
    for containerid, (item, text) in enumerate(
            bounds,
            start=xoff,
    ):
        # TODO: INVESTIGATE LAST ONE
        distanceid = containerid - xoff + 1
        # font = fontstore.font(page, containerid, line=0, char=0)
        splitted = text.splitlines()
        if len(splitted) > 1:
            continue
        fontsize = fontsize_from_textbounds(item)

        fontdistance = distances[distanceid]

        headline_tosmall = fontsize <= smallest_headlinesize
        distance_tosmall = fontdistance <= smallest_headlinedistance
        if (headline_tosmall and distance_tosmall) or distance_tosmall:
            continue

        try:
            # TODO: IMPROVE LEVEL CALCULATION
            # Space after and before
            level = distances[distanceid] + distances[distanceid + 1]
        except IndexError:
            level = distances[distanceid] * 2
        headline = Headline(
            container=containerid,
            level=level,
            page=page,
            text=text,
        )
        result.append(headline)
    return result


def prepare_chapter_and_content(sections_, chapter):
    assert isinstance(sections_, sections.feature.sections.Sections)
    assert sections_, 'no sections provided'
    if chapter is None:
        # process all chapter
        # TODO: clearify code
        content = determine_content_border(sections_)
        chapter = list(range(len(content)))
    else:
        content = sections.feature.sections.chapters(sections_)
        chapter = [chapter] if isinstance(chapter, int) else chapter
    return chapter, content


def contentborder(sizeandborder, horizontals):
    contentborders = [item.border for item in sizeandborder]
    border = content_border(horizontals, contentborders)
    assert border.bottom >= 100, str(border)
    return border


def determine_content_border(items):
    # analyze all chapter of the document
    contents = [
        item for item in items
        if isinstance(item, sections.feature.sections.Content)
    ]
    # support more than one content element
    chapters = [[
        chapter
        for chapter in content.content
        if isinstance(chapter, iamraw.sections.Chapter)
    ]
                for content in contents]
    chapters = utila.flatten(chapters)

    if not chapters:
        # TODO: INVESTIGATE HERE
        return []

    result = []
    for current, after in zip(chapters[:-1], chapters[1:]):
        # TODO: check after.start - 1 later
        result.append((current.start, after.start - 1))
    result.append((chapters[-1].start, contents[-1].end))

    # ensure ascending page numbers
    assert all([start <= end for start, end in result]), str(result)
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
    # TODO: check this approach
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
