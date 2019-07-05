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
    print(chapter.title)
    for paragraph in chapter:
        print(paragraph.title)
        print(paragraph.number)
        for sentence in paragraph:
            print('word cout: %d' % len(sentence))
            for word in sentence:
                print(word)

word

word.font
word.font.color
word.font.size
word.style = [i, b, u, strong? etc?]
"""

from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from itertools import zip_longest
from re import finditer
from typing import List

from iamraw import Border
from serializeraw import load_boxes
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_pageborders
from utila import NEWLINE
from utila import from_raw_or_path
from utila import logging_error
from yaml import FullLoader
from yaml import dump
from yaml import load

from groupme.feature.numbers import load_textposition
from hey.fonts.store import FontContentStore
from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from hey.textnavigator.navigator import PageTextContentNavigator
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import PageTextNavigators
from hey.textnavigator.navigator import create_pagetextnavigators
from hey.utils import flatten
from words.feature.headlines import Headline
from words.feature.headlines import content_border
from words.feature.headlines import load_headlines


@dataclass
class Content:
    content: object


@dataclass
class Paragraph(Content):
    pass


@dataclass
class BoxedContent(Content):
    boxid: int = field(default=-1)


@dataclass
class Undefined(Content):
    container: int = field(default=-1)
    content: str = None


@dataclass
class NoParagraph(Content):
    pass


ChapterText = List[Content]


class BoxedChecker:
    # TODO: VERY SLOW, REPLACE WITH GOOD ONE, FOR THE FIRST TIME, TIME IS NOT
    # IMPORTANT.
    def __init__(self, boxes):
        self.data = []
        for page in boxes:
            content = []
            for box in page:
                bounding = box.box
                content.append(bounding)
            self.data.append(content)

    def contains(self, page, bounds) -> int:
        return self.boxid(page, bounds) >= 0

    def boxid(self, page, bounds) -> int:
        y0, x0, y1, x1 = bounds
        for index, bound in enumerate(self.data[page]):
            _y0, _x0, _y1, _x1 = bound
            if _y0 <= y0 <= y1 <= _y1 and _x0 <= x0 <= x1 <= _x1:
                return index
        return -1


def work(
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        headlines: str,
        pagesizes: str,
        horizontals: str,
        boxes: str,
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
    border, fontstore, headlines, textnavigators, boxes = prepare_input(
        text=text,
        text_position=text_position,
        font_header=font_header,
        font_content=font_content,
        headlines=headlines,
        pagesizes=pagesizes,
        horizontals=horizontals,
        boxes=boxes,
    )

    extracted = extract_texts(
        border=border,
        fontstore=fontstore,
        headlines=headlines,
        textnavigators=textnavigators,
        boxes=boxes,
    )

    dumped = dump_text(extracted)
    return dumped


def prepare_input(
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        headlines: str,
        pagesizes: str,
        horizontals: str,
        boxes: str,
):
    """Load content from path and create required object"""
    text = load_document(text)
    position = load_textposition(text_position)
    headlines = load_headlines(headlines)
    horizontals = load_horizontals(horizontals)
    boxes = load_boxes(boxes)
    fontstore = create_fontstore(font_header, font_content)
    textnavigators = create_pagetextnavigators(position, text)
    _, contentborder = load_pageborders(pagesizes)
    border = content_border(horizontals, contentborder)
    boxes = BoxedChecker(boxes)
    return border, fontstore, headlines, textnavigators, boxes


def extract_texts(
        headlines,
        fontstore: FontStore,
        textnavigators: PageTextNavigators,
        border: Border,
        boxes: BoxedChecker,
):
    result = []
    for headline in headlines:
        analyzed = analyze_page(
            headline,
            fontstore,
            textnavigators,
            border,
            boxes,
        )
        result.append(analyzed)
    result = squeeze_text(result)

    return result


NEW_SENTENCE = [
    r'[\w|>|<]\. ',  # TODO: add more special chars
    r'[\w|>|<]\.$',
    r'\? ',
    r'\?$',
    r'\w: ',
    r'\w:$',
]
PATTERN = '|'.join(NEW_SENTENCE)


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


def squeeze_text_page(page):
    result = []
    for (headline, sequence) in page:
        lines = []
        for seq in sequence:
            if not isinstance(seq, Paragraph):
                lines.append('%du' % seq.container)
                continue
            line = ''.join([item for (item, _) in seq.content])
            line = line.replace(NEWLINE, SPACE)
            last = 0
            for item in finditer(PATTERN, line):
                _, end = item.start(), item.end()
                lines.append(line[last:end])
                last = end
            no_match = line == line[last:]
            if no_match:
                logging_error('No match, potential headline: %s' % line)
            if line[last:]:
                lines.append(line[last:])
        # remove `space` after text
        lines = [item.strip() for item in lines]
        result.append((
            headline,
            lines,
        ))
    return result


def analyze_page(
        content,
        fontstore: FontStore,
        textnavigators: PageTextNavigator,
        border: Border,
        boxes: BoxedChecker,
):
    assert content, 'empty `content`'
    page = content[0].page
    pcn = PageTextContentNavigator(
        textnavigator=textnavigators[page],
        content=border,
    )
    fontstore = FontContentStore(fontstore, pcn, page)

    if content[0].container > pcn.offset[0]:
        # the page does not start with a headline, without inserting an empty
        # line the starting content of the page is ignored
        # -> add starting container
        headline = Headline(
            text=None,
            level=None,
            rawlevel=None,
            page=page,
            container=pcn.offset[0],
        )
        content = [headline] + content
    result = []
    for first, second in zip_longest(content, content[1:], fillvalue=None):
        start = first.container + 1
        # determine end mark
        end = len(pcn)
        if second and first.page == second.page:
            end = second.container - 1
        # collect content after headline
        collector = []
        for index in range(start, end):
            _bounding, _content = pcn[index]  # bounding, content
            fonts = fontstore.fromstr(index, 0, _content)
            contenttype = content_type(boxes, page, _bounding, _content)
            if contenttype == ContentType.PARAGRAPH:
                collector.append(Paragraph(content=fonts))
            else:
                collector.append(Undefined(container=index))
        result.append((first, collector))

    return (page, result)


# TODO: Remove duplication
DOT = '•'


class ContentType(Enum):
    UNDEFINED = 0
    PARAGRAPH = 1
    BOXED = 2
    LIST = 3


def content_type(boxed: BoxedChecker, page: int, bounding, content):
    if DOT in content:
        return ContentType.LIST
    if boxed.contains(page, bounding):
        return ContentType.BOXED
    return ContentType.PARAGRAPH


def dump_text(text: List[ChapterText]) -> str:
    raw = []
    index = 0
    for (page, content) in text:
        collector = []
        for headline, headline_content in content:
            current = {
                # placeholder headline
                'headline': None,
                'fc': headline.container,
                'content': [],
            }
            if headline.text is not None:
                current['headline'] = index
                index += 1
            for oneline in headline_content:
                current['content'].append(oneline)
            collector.append(current)
        raw.append({
            'page': page,
            'content': collector,
        })
    dumped = dump(raw)
    return dumped


def load_text(content: str, headlines) -> List[ChapterText]:
    """Load text and replace headline reference with current headline

    Args:
        content(str): path to dumped text
        headlines(List[List[Headline]]): list of page with list of headlines
    Returns:
        loaded text with replaced headlines
    """
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    # convert page index to global index
    headlines = flatten(headlines)

    result = []
    for line in loaded:
        page, content = line['page'], line['content']
        pagecontent = []
        for section in content:
            section_content, headline = section['content'], section['headline']
            headline = headlines[headline] if headline is not None else None
            if headline is None:
                headline = Headline(
                    text=None,
                    level=None,
                    rawlevel=None,
                    page=page,
                    container=section['fc'])
            pagecontent.append((headline, section_content))

        result.append((page, pagecontent))
    return result
