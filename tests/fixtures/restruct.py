# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw import Document
from pytest import fixture
from serializeraw import load_boxes
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_pageborders

from groupme.feature.numbers import load_textposition
from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from hey.textnavigator.navigator import create_pagetextnavigators
from sections.creator import add_chapter
from sections.creator import add_content
from sections.creator import add_index
from sections.creator import add_introduction
from sections.creator import add_table
from sections.creator import add_text
from sections.creator import add_title
from sections.creator import add_toc
from sections.creator import add_whitepage
from sections.ctor import PERCENT_100
from sections.ctor import Sections
from sections.feature.chapter import work as chapter_work
from sections.feature.index import work as index_work
from sections.feature.sections import work as section_work
from sections.feature.title import work as title_work
from sections.feature.toc import work as toc_work
from sections.feature.whitepage import work as whitepage_work
from tests.resources import RESTRUCT_BOXES
from tests.resources import RESTRUCT_FONT_CONTENT
from tests.resources import RESTRUCT_FONT_HEADER
from tests.resources import RESTRUCT_HORIZONTAL
from tests.resources import RESTRUCT_ONELINE_FONT_CONTENT
from tests.resources import RESTRUCT_ONELINE_FONT_HEADER
from tests.resources import RESTRUCT_ONELINE_TEXT
from tests.resources import RESTRUCT_PAGESIZE
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TEXT_POSITION
from tests.resources import RESTRUCT_TOC
from words.feature.boxed import dump_boxedcontent
from words.feature.boxed import prepare_input as boxed_prepare_input
from words.feature.boxed import process_content as boxed_process_content
from words.feature.headlines import content_border
from words.feature.headlines import work as headlines_work
from words.feature.list import dump_lists
from words.feature.list import prepare_input as list_prepare_input
from words.feature.list import process as list_process
from words.feature.text import dump_text
from words.feature.text import extract_texts as text_extract_texts
from words.feature.text import prepare_input as text_prepare_input


@fixture
def restructured():
    pagesize = load_pageborders(RESTRUCT_PAGESIZE)
    horizontals = load_horizontals(RESTRUCT_HORIZONTAL)
    position = load_textposition(RESTRUCT_TEXT_POSITION)
    document = load_document(RESTRUCT_TEXT)

    assert pagesize
    assert horizontals
    assert position

    assert len(position) == len(document)
    assert len(horizontals) == len(document)

    navigators = create_pagetextnavigators(
        text=document,
        text_position=position,
    )
    return navigators, horizontals


@fixture
def restructured_chapter():
    result = chapter_work(RESTRUCT_TEXT, RESTRUCT_TEXT_POSITION, RESTRUCT_TOC)
    return result


@fixture
def restructured_text() -> Document:
    loaded = load_document(RESTRUCT_TEXT)
    return loaded


@fixture
def restructured_fontstore() -> FontStore:
    lookup = create_fontstore(RESTRUCT_FONT_HEADER, RESTRUCT_FONT_CONTENT)
    return lookup


def restructured_fontstore_fixture() -> FontStore:
    # TODO: Remove with new pytest - this is required, because pytest carn't
    # use fixture in paramertized tests.
    lookup = create_fontstore(RESTRUCT_FONT_HEADER, RESTRUCT_FONT_CONTENT)
    return lookup


@fixture
def restructured_horizontals():
    loaded = load_horizontals(RESTRUCT_HORIZONTAL)
    return loaded


@fixture
def restructured_index():
    result = index_work(RESTRUCT_ONELINE_TEXT)
    return result


@fixture
def restructured_navigator(restructured):  #pylint:disable=W0621
    navigators, _ = restructured
    return navigators


@fixture
def restructured_headlines():
    sections_ = restructured_sections()
    dumped = headlines_work(
        sections=sections_,
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
        font_header=RESTRUCT_FONT_HEADER,
        font_content=RESTRUCT_FONT_CONTENT,
        sizeandborder=RESTRUCT_PAGESIZE,
        horizontals=RESTRUCT_HORIZONTAL,
    )
    return dumped


@fixture
def restructured_sections_manual() -> Sections:
    result = Sections()

    def analyse(section, start, end):
        return section(result, start, end, PERCENT_100)
        # TODO: reactivate [start, START] later
        # return section(result, [start, START], [end, END], PERCENT_100)

    def add_children(parent, ctor, start, end):
        # new = ctor(parent, [start, START], [end, END], PERCENT_100)
        new = ctor(parent, start, end, PERCENT_100)
        return new

    # Page, Start
    # Intro
    intro = analyse(add_introduction, 0, 1)
    add_children(intro, add_title, 0, 0)
    add_children(intro, add_whitepage, 1, 1)

    # First pages with tables
    table_first = analyse(add_table, 2, 5)
    add_children(table_first, add_toc, 2, 2)
    add_children(table_first, add_whitepage, 3, 3)
    add_children(table_first, add_text, 4, 4)
    add_children(table_first, add_whitepage, 5, 5)

    # Content starts here
    content = analyse(add_content, 6, 25)
    add_chapter(content, 6, 7, number=1)
    add_chapter(content, 8, 9, number=2)
    add_chapter(content, 10, 11, number=3)
    add_chapter(content, 12, 17, number=4)
    add_chapter(content, 18, 19, number=5)
    add_chapter(content, 20, 21, number=6)
    add_chapter(content, 22, 23, number=7)
    add_chapter(content, 24, 25, number=8)

    # Second pages with table
    table_second = analyse(add_table, 26, 26)
    add_children(table_second, add_index, 26, 26)

    return result


@fixture
def restructured_sizeandborder():
    size, border = load_pageborders(RESTRUCT_PAGESIZE)
    return size, border


@fixture
def restructured_text_positions():
    loaded = load_textposition(RESTRUCT_TEXT_POSITION)
    return loaded


@fixture
def restructured_title():
    result = title_work(
        RESTRUCT_ONELINE_TEXT,
        RESTRUCT_ONELINE_FONT_HEADER,
        RESTRUCT_ONELINE_FONT_CONTENT,
    )
    return result


@fixture
def restructured_toc():
    result = toc_work(RESTRUCT_ONELINE_TEXT)
    return result


def restructured_text_fixture() -> Document:
    loaded = load_document(RESTRUCT_TEXT)
    return loaded


@fixture
def restructured_whitepage():
    result = whitepage_work(
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        RESTRUCT_HORIZONTAL,
    )
    return result


def restructured_sections():
    chapter = chapter_work(RESTRUCT_TEXT, RESTRUCT_TEXT_POSITION, RESTRUCT_TOC)

    index = index_work(RESTRUCT_TEXT)
    title = title_work(
        RESTRUCT_TEXT,
        RESTRUCT_FONT_HEADER,
        RESTRUCT_FONT_CONTENT,
    )
    toc = toc_work(RESTRUCT_TEXT)
    whitepage = whitepage_work(
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        RESTRUCT_HORIZONTAL,
    )
    result = section_work(chapter, index, title, toc, whitepage)
    return result


@fixture
def restructured_textexample(
        # pylint:disable=W0621
        restructured_headlines):
    headlines = restructured_headlines
    border, fontstore, headlines, textnavigators, boxes = text_prepare_input(
        text=RESTRUCT_TEXT,
        text_position=RESTRUCT_TEXT_POSITION,
        font_header=RESTRUCT_FONT_HEADER,
        font_content=RESTRUCT_FONT_CONTENT,
        headlines=headlines,
        pagesizes=RESTRUCT_PAGESIZE,
        horizontals=RESTRUCT_HORIZONTAL,
        boxes=RESTRUCT_BOXES,
    )

    extracted = text_extract_texts(
        border=border,
        fontstore=fontstore,
        headlines=headlines,
        textnavigators=textnavigators,
        boxes=boxes,
    )
    assert extracted is not None
    return extracted


@fixture
def restructured_textexample_dumped(
        # pylint:disable=W0621
        restructured_textexample) -> str:
    return dump_text(restructured_textexample)


@fixture
def restructured_border():
    _, border = load_pageborders(RESTRUCT_PAGESIZE)
    return border


@fixture
def restructured_boxed(
        # pylint:disable=W0621
        restructured_textexample_dumped,
        restructured_headlines,
):
    headlines = restructured_headlines
    undefined = restructured_textexample_dumped

    extracted, _ = boxed_prepare_input(
        undefined,
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        border=RESTRUCT_PAGESIZE,
        headlines=headlines,
        horizontals=RESTRUCT_HORIZONTAL,
    )
    boxes = load_boxes(RESTRUCT_BOXES)

    result = boxed_process_content(extracted, boxes)
    return result


@fixture
def restructured_boxed_dumped(
        # pylint:disable=W0621
        restructured_boxed) -> str:
    dumped = dump_boxedcontent(restructured_boxed)
    return dumped


@fixture
def restructured_contentborder(
        # pylint:disable=W0621
        restructured_horizontals,
        restructured_border,
):
    horizontals = restructured_horizontals
    border = restructured_border
    result = content_border(horizontals, border)
    return result


@fixture
def restructured_list_work(
        restructured_textexample_dumped,
        restructured_headlines,
):
    headlines = restructured_headlines
    undefined = restructured_textexample_dumped

    extracted, contentborder = list_prepare_input(
        undefined,
        RESTRUCT_TEXT,
        RESTRUCT_TEXT_POSITION,
        headlines=headlines,
        border=RESTRUCT_PAGESIZE,
        horizontals=RESTRUCT_HORIZONTAL,
    )
    result = list_process(extracted, contentborder)
    return result


@fixture
def restructured_list_dumped(
        # pylint:disable=W0611
        restructured_list_work) -> str:
    result = restructured_list_work
    dumped = dump_lists(result)
    return dumped
