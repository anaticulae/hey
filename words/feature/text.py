# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
.. code-block:: python

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

import collections
import dataclasses
import functools
import itertools
import re
import typing

import iamraw
import serializeraw
import utila

import hey.fonts.store
import hey.textnavigator.navigator
import words.boxed
import words.feature
import words.headlines


def work(
        text: str,
        textposition: str,
        fontheader: str,
        fontcontent: str,
        headlines: str,
        pagesizes: str,
        boxes: str,
        headerfooters: str,
        pages: tuple = None,
) -> str:
    """Extract text paragraphs from document

    Args:
        text(str): path to text extraction from rawmaker
        textposition(str): path to textposition matching with text-extraction
        fontheader(str): table with all fonts in document
        fontcontent(str): font definition for every word
        headlines(str): path to extracted headlines from hey/words
        pagesizes(str): path to size and border
        boxes(str): definition of boxed rectangles
        headerfooters: path to extracted footer and header
        pages: list of page numbers to process
    Returns:
        dumped paragraphs
    """
    resources = words.feature.load_resources(
        boxes=boxes,
        fontcontent=fontcontent,
        fontheader=fontheader,
        headerfooters=headerfooters,
        headlines=headlines,
        pagesizes=pagesizes,
        text=text,
        textposition=textposition,
        pages=pages,
    )

    extracted = extract_texts(resources)

    dumped = serializeraw.dump_text(extracted)
    return dumped


@dataclasses.dataclass
class HeadlineWithContent:
    text: str = None
    content: typing.List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class PageTextWithHeadlines:
    page: int = None
    content: typing.List[HeadlineWithContent] = dataclasses.field(default_factory=list) # yapf:disable


def extract_texts(loaded: words.feature.TextRequiredResources):
    result = []
    # ensure to preserve correct page order when having pages without headline
    headlines = insert_empty_pages(loaded.headlines)
    # start analyzing
    for headline in headlines:
        analyzed = analyze_page(
            headline,
            loaded.fontstore,
            loaded.textnavigators,
            loaded.border,
            loaded.boxes,
        )
        if analyzed is None:
            # empty page
            continue
        result.append(analyzed)
    result = squeeze_text(result)
    return result


def analyze_page(
        headlines,
        fontstore: hey.fonts.store.FontStore,
        textnavigators: hey.textnavigator.navigator.PageTextNavigator,
        border: iamraw.Border,
        boxes: words.boxed.BoxedChecker,
) -> typing.Tuple[iamraw.PageNumber, iamraw.Paragraphs]:
    """ """
    assert headlines, 'empty `headlines`'
    # TODO: Remove try/except
    prepared = prepare_analyze_page(
        headlines,
        textnavigators,
        fontstore,
        border,
    )
    if prepared is None:
        # Skip analyzing empty pages
        return None

    # prepare collection
    page, headlines, pcn, fcs = prepared
    call = functools.partial(
        collect_paragraph,
        page=page,
        pcn=pcn,
        fcs=fcs,
        boxes=boxes,
    )
    zipped = itertools.zip_longest(headlines, headlines[1:], fillvalue=None)

    # collect paragraphs
    result = [
        (first, call(first=first, second=second)) for (first, second) in zipped
    ]

    # clear result, remove empty content
    result = [(headline, content)
              for (headline, content) in result
              if (headline.container is not None and headline.container > -1)]
    return (page, result)


def squeeze_text(containers: typing.List[PageTextWithHeadlines]):
    """
    `Containers` represents the chapter structure.
    """
    result = []
    for number, pagecontent in containers:
        pageresult = squeeze_text_page(pagecontent)
        result.append((number, pageresult))
    return result


def collect_paragraph(
        first: iamraw.Headline,
        second: iamraw.Headline,
        page: int,
        pcn: hey.textnavigator.navigator.PageTextContentNavigator,
        fcs: hey.fonts.store.FontContentStore,
        boxes: words.boxed.BoxedChecker,
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
    result = []
    for index in range(start, end):
        _bounding, _content = pcn[index].bounding, pcn[index].text
        try:
            # TODO: INVESTIGATE WHATS WRONG HERE
            fonts = fcs.fromstr(index, 0, _content)
        except KeyError:
            fonts = None
        contenttype = content_type(boxes, page, _bounding, _content)
        if contenttype == iamraw.ContentType.PARAGRAPH:
            result.append(iamraw.Paragraph(content=fonts))
        else:
            result.append(iamraw.Undefined(container=index))
    return result


def prepare_analyze_page(
        headlines,
        textnavigators,
        fontstore,
        borders,
):
    """Add dummy headline if required

    Some pages does not contain a headline or the headline starts after
    the first text content. Therefore adding a dummy headline is
    required to collect this content under the dummy headline.

    Args:

    """
    page = headlines[0].page
    content = utila.select_page(borders, page=page)
    if content is None:
        return None

    pcn = hey.textnavigator.navigator.PageTextContentNavigator(
        textnavigator=utila.select_page(textnavigators, page=page),
        content=utila.select_page(borders, page=page),
    )
    if pcn.offset == (None, None):
        # empty page
        return None

    fontstore = hey.fonts.store.FontContentStore(fontstore, pcn, page)
    # pcn.offset[0] - 1: the "virtual" headline is one container element before
    # the first content.
    if headlines[0].container is None:
        # start with None-Container
        headlines[0].container = pcn.offset[0] - 1  # absolute coordinate
    elif headlines[0].container > pcn.offset[0]:
        # the page does not start with a headline, without inserting an empty
        # line the starting content of the page is ignored
        # -> add starting container
        headline = iamraw.Headline(
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


def insert_empty_pages(headlines):
    """Add pages with content but without any headlines.

    What happens when we forget to fill the headlines? All pages without any
    headlines are ignored in content analyzis.
    """
    # fill headlines
    heads = []
    for first, second in itertools.zip_longest(
            utila.flatten(headlines),
            utila.flatten(headlines)[1:],
            fillvalue=None,
    ):
        heads.append(first)
        if second is None:
            utila.error('Implement fill last one till chapter ends')
            break
        for index in range(first.page + 1, second.page):
            heads.append(iamraw.Headline(text=None, level=None, page=index))

    headlines = [
        list(group) for _, group in itertools.groupby(heads, lambda x: x.page)
    ]
    return headlines


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
            if not isinstance(seq, iamraw.Paragraph):
                lines.append('%du' % seq.container)
                continue
            # skip here to ensure that Undefined Container is added which
            # does not have any content, see commit.
            if seq.content is None:
                continue
            line = ''.join([item for (item, _) in seq.content])
            line = line.replace(utila.NEWLINE, SPACE)
            last = 0
            for item in re.finditer(PATTERN, line):
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
    if iamraw.DOT in content:
        return iamraw.ContentType.LIST
    if boxed.contains(page, bounding):
        return iamraw.ContentType.BOXED
    return iamraw.ContentType.PARAGRAPH


EmptyPage = collections.namedtuple('EmptyPage', 'page')
