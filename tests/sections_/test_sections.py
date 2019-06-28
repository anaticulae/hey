# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture
from pytest import mark
from serializeraw import load_likelihood

# from sections.sections import extract_sections
from sections.creator import add_chapter
from sections.creator import add_content
from sections.creator import add_index
from sections.creator import add_introduction
from sections.creator import add_table
from sections.creator import add_text
from sections.creator import add_title
from sections.creator import add_toc
from sections.creator import add_whitepage
from sections.creator import validate
from sections.ctor import PERCENT_100
from sections.ctor import Sections
from sections.feature.chapter import load_chapter_detection
from sections.feature.sections import chapters
from sections.feature.sections import extract_sections
from sections.feature.whitepage import load_whitepages
from sections.feature.whitepage import whitepage_value_to_percent
from sections.serialize import dump_sections
from sections.serialize import load_sections
#pylint:disable=W0611
from tests.sections_.test_chapter import restructured_chapter
from tests.sections_.test_index import restructured_index
from tests.sections_.test_title import restructured_title
from tests.sections_.test_toc import restructured_toc
from tests.sections_.test_whitepage import restructured_whitepage

#     assert extracted == restructured


@fixture
def restructured() -> Sections:
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


def test_sections_iterable():
    """Create empty `Sections` and iterate over `Sections` and `AreaItem`s"""
    document = Sections()
    for section in document:
        len(section)
        for item in section:  #pylint:disable=unused-variable
            pass


@mark.xfail(reason='not fully implemented')
def test_sections_dump_and_load_sections(restructured):  #pylint:disable=W0621
    data = restructured

    dumped = dump_sections(data)
    assert dumped

    loaded = load_sections(dumped)
    assert loaded

    assert loaded == data


def test_validate_restructured(restructured):  #pylint:disable=W0621
    validated = validate(restructured)
    assert validated


#pylint:disable=W0621
def test_sections_extract_sections(
        restructured_chapter,
        restructured_index,
        restructured_title,
        restructured_toc,
        restructured_whitepage,
        restructured,
):
    chapter = load_chapter_detection(restructured_chapter)
    index = load_likelihood(restructured_index)
    title = load_likelihood(restructured_title)
    toc = load_likelihood(restructured_toc)
    whitepage = load_whitepages(restructured_whitepage)
    whitepage = [whitepage_value_to_percent(item) for item in whitepage]

    source = [chapter, index, title, toc, whitepage]
    result = extract_sections(*source)
    assert result

    for index, (actual, expected) in enumerate(zip(result, restructured)):
        print('check level %d' % index)
        # Compare only the first level
        assert actual.start == expected.start
        assert actual.end == expected.end

    # TODO: activate later, do not want to make this test so explicit
    # assert result == restructured


def test_sections_chapters(restructured):
    result = chapters(restructured)

    # start is lower or equal than end page size
    # start = item[0]
    # end   = item[1]
    ascending_page_order = all([item[0] <= item[1] for item in result])

    assert ascending_page_order, str([result])
    assert len(result) == 8, str(result)
