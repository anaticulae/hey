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

from sections.creator import add_chapter
from sections.creator import add_content
from sections.creator import add_index
from sections.creator import add_introduction
from sections.creator import add_table
from sections.creator import add_title
from sections.creator import add_toc
from sections.creator import add_whitepage
from sections.ctor import END
from sections.ctor import PERCENT_100
from sections.ctor import START
from sections.ctor import Sections
from sections.sections import extract_sections
from sections.sections import validate
from sections.serialize import dump_sections
from sections.serialize import load_sections


@fixture
def restructured() -> Sections:
    result = Sections()

    def analyse(section, start, end):
        return section(result, [start, START], [end, END], PERCENT_100)

    def add_children(parent, ctor, start, end):
        new = ctor(parent, [start, START], [end, END], PERCENT_100)
        return new

    # Page, Start
    # Intro
    intro = analyse(add_introduction, 0, 1)
    add_children(intro, add_title, 0, 0)
    add_children(intro, add_whitepage, 0, 0)

    # First pages with tables
    table_first = analyse(add_table, 2, 3)
    add_children(table_first, add_toc, 2, 2)

    # Content starts here
    content = analyse(add_content, 4, 25)
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
def test_dump_and_load_sections(restructured):  #pylint:disable=W0621
    data = restructured

    dumped = dump_sections(data)

    loaded = load_sections(dumped)

    assert loaded == data


def test_validate_restructured(restructured):  #pylint:disable=W0621
    validated = validate(restructured)
    assert validated


@mark.xfail(reason='not fully implemented')
def test_structure_document(restructured):  #pylint:disable=W0621
    extracted = extract_sections()

    assert extracted == restructured
