# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""

for chapter in content:
    p(chapter.title)
    for paragraph in chapter:
        p(paragraph.title)
        p(paragraph.number)
        for sentence in paragraph:
            p('word cout: %d' % len(sentence))
            for word in sentence:
                p(word)

word

word.font
word.font.color
word.font.size
word.style = [i, b, u, strong? etc?]
"""

from functools import partial
from itertools import groupby
from itertools import zip_longest
from re import finditer
from typing import Tuple

import serializeraw
import utila
from iamraw import DOT
from iamraw import Border
from iamraw import ContentType
from iamraw import Headline
from iamraw import PageNumber
from iamraw import Paragraph
from iamraw import Paragraphs
from iamraw import Undefined

import words.boxed
import words.feature
import words.headlines
from hey.fonts.store import FontContentStore
from hey.fonts.store import FontStore
from hey.textnavigator.navigator import PageTextContentNavigator
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import PageTextNavigators


def work(
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        headlines: str,
        pagesizes: str,
        boxes: str,
        headerfooters: str,
        pages=None,
) -> str:
    """Extract text paragraphs from document

    Args:
        text(str): path to text extraction from rawmaker
        text_position(str): path to text_position matching with text-extraction
        font_header(str):
        font_content(str):
        headlines(str): path to extracted headlines from hey/words
        pagesizes(str):
        horizontals(str):
    Returns:
        dumped paragraphs
    """
    resources = words.feature.load_resources(
        boxes=boxes,
        font_content=font_content,
        font_header=font_header,
        headerfooters=headerfooters,
        headlines=headlines,
        pagesizes=pagesizes,
        text=text,
        text_position=text_position,
        pages=pages,
    )

    extracted = extract_texts(*resources)

    dumped = serializeraw.dump_text(extracted)
    return dumped


def analyze_page(
        headlines,
        fontstore: FontStore,
        textnavigators: PageTextNavigator,
        border: Border,
        boxes: words.boxed.BoxedChecker,
) -> Tuple[PageNumber, Paragraphs]:
    """ """
    assert headlines, 'empty `headlines`'
    # TODO: Remove try/except
    try:
        prepared = prepare_analyze_page(
            headlines,
            textnavigators,
            fontstore,
            border,
        )
    except EmptyPageError as emptypage:
        # Skip analyzing empty pages
        return (emptypage.page, None)

    # prepare collection
    page, headlines, pcn, fcs = prepared
    call = partial(collect_paragraph, page=page, pcn=pcn, fcs=fcs, boxes=boxes)
    zipped = zip_longest(headlines, headlines[1:], fillvalue=None)

    # collect paragraphs
    result = [
        (first, call(first=first, second=second)) for (first, second) in zipped
    ]

    # clear result, remove empty content
    result = [(headline, content)
              for (headline, content) in result
              if (headline.container is not None and headline.container > -1)]
    return (page, result)


def collect_paragraph(
        first: Headline,
        second: Headline,
        page: int,
        pcn: PageTextContentNavigator,
        fcs: FontContentStore,
        boxes,
):
    """
    Hint: The Headlines/Container are numbered in absolute indies. Accessing
    the content requires to subtract the offset which is produced by the
    header.
    """
    # convert to content coordiante, and step one element further cause of
    # current element is the headline and we want to start with content
    start = first.container + 1 - pcn.offset[0]
    # determine end mark
    if second and first.page == second.page:
        end = second.container - 1
    else:
        end = len(pcn)
    # collect content after headline
    collector = []
    for index in range(start, end):
        _bounding, _content = pcn[index]  # bounding, content
        fonts = fcs.fromstr(index, 0, _content)
        contenttype = content_type(boxes, page, _bounding, _content)
        if contenttype == ContentType.PARAGRAPH:
            collector.append(Paragraph(content=fonts))
        else:
            collector.append(Undefined(container=index))
    return collector


def prepare_analyze_page(
        headlines,
        textnavigators,
        fontstore,
        borders,
):
    """Add dummy headline if required

    Some pages does not contain a headline or the headline starts after the
    first text content. Therefore add dummy headline is required to collect
    this content under the dummy headline.

    Args:

    """
    page = headlines[0].page
    pcn = PageTextContentNavigator(
        textnavigator=utila.select_page(textnavigators, page=page),
        content=utila.select_page(borders, page=page),
    )
    if pcn.offset == (None, None):
        # empty page
        raise EmptyPageError(page)
    fontstore = FontContentStore(fontstore, pcn, page)
    # pcn.offset[0] - 1: the "virtual" headline is one container element before
    # the first content.
    if headlines[0].container is None:
        # start with None-Container
        headlines[0].container = pcn.offset[0] - 1  # absolute coordinate
    elif headlines[0].container > pcn.offset[0]:
        # the page does not start with a headline, without inserting an empty
        # line the starting content of the page is ignored
        # -> add starting container
        headline = Headline(
            text=None,
            level=None,
            rawlevel=None,
            page=page,
            container=pcn.offset[0] - 1,  # absoulte coordinate
        )
        headlines = [headline] + headlines
    else:
        # normal headline
        pass
    return page, headlines, pcn, fontstore


def extract_texts(
        border: Border,
        boxes: words.boxed.BoxedChecker,
        fontstore: FontStore,
        headlines,
        textnavigators: PageTextNavigators,
):
    result = []

    # fill headlines
    headlines = fill_headlines(headlines)
    # start analyzing
    for headline in headlines:
        analyzed = analyze_page(
            headline,
            fontstore,
            textnavigators,
            border,
            boxes,
        )
        _, content = analyzed
        if not content:
            continue
        result.append(analyzed)
    result = squeeze_text(result)
    return result


def fill_headlines(headlines):
    """Add pages with content but without any headlines.

    What happens when we forget to fill the headlines? All pages without any
    headlines are ignored in content analyzis.
    """
    # fill headlines
    heads = []
    for first, second in zip_longest(
            utila.flatten(headlines),
            utila.flatten(headlines)[1:],
            fillvalue=None,
    ):
        heads.append(first)
        if second is None:
            utila.error('Implement fill last one till chapter ends')
            break
        for index in range(first.page + 1, second.page):
            heads.append(Headline(text=None, level=None, page=index))

    headlines = [list(group) for _, group in groupby(heads, lambda x: x.page)]
    return headlines


def squeeze_text(containers):
    """
    `Containers` represents the chapter structure.
    """
    result = []
    for number, pagecontent in containers:
        pageresult = squeeze_text_page(pagecontent)
        result.append((number, pageresult))
    return result


SPACE = ' '

# TODO: add more special chars
SPECIAL_CHARS = ['>', '<', r'\)', r'\(']
SPECIAL_CHARS = '|'.join(SPECIAL_CHARS)

NEW_SENTENCE = [
    r'[\w' + SPECIAL_CHARS + r']\. ',
    r'[\w' + SPECIAL_CHARS + r']\.$',
    r'\? ',
    r'\?$',
    r'\w: ',
    r'\w:$',
]
PATTERN = '|'.join(NEW_SENTENCE)


def squeeze_text_page(page):

    result = []
    for (headline, sequence) in page:
        lines = []
        for seq in sequence:
            if not isinstance(seq, Paragraph):
                lines.append('%du' % seq.container)
                continue
            line = ''.join([item for (item, _) in seq.content])
            line = line.replace(utila.NEWLINE, SPACE)
            last = 0
            for item in finditer(PATTERN, line):
                _, end = item.start(), item.end()
                lines.append(line[last:end])
                last = end
            no_match = line == line[last:]
            if no_match:
                utila.error('No match, potential headline: %s' % line)
            if line[last:]:
                lines.append(line[last:])
        # remove `space` after text
        lines = [item.strip() for item in lines]
        result.append((
            headline,
            lines,
        ))
    return result


def content_type(boxed: words.boxed.BoxedChecker, page: int, bounding, content):
    if DOT in content:
        return ContentType.LIST
    if boxed.contains(page, bounding):
        return ContentType.BOXED
    return ContentType.PARAGRAPH


class EmptyPageError(ValueError):
    """Page contains no content but maybe header and/or footer"""

    def __init__(self, page):
        super().__init__()
        self.page = page
