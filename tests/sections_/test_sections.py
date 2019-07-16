# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import xfail
from serializeraw import load_likelihood

# from sections.sections import extract_sections
from sections.creator import validate
from sections.ctor import Sections
from sections.feature.chapter import load_chapter_detection
from sections.feature.sections import chapters
from sections.feature.sections import extract_sections
from sections.feature.whitepage import load_whitepages
from sections.feature.whitepage import whitepage_value_to_percent
from sections.serialize import dump_sections
from sections.serialize import load_sections
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_chapter
from tests.fixtures.restruct import restructured_index
from tests.fixtures.restruct import restructured_sections_manual
from tests.fixtures.restruct import restructured_title
from tests.fixtures.restruct import restructured_toc
from tests.fixtures.restruct import restructured_whitepage
from tests.fixtures.simple import simple_chapter
from tests.fixtures.simple import simple_index
from tests.fixtures.simple import simple_sections
from tests.fixtures.simple import simple_title
from tests.fixtures.simple import simple_toc
from tests.fixtures.simple import simple_whitepage


def test_sections_iterable():
    """Create empty `Sections` and iterate over `Sections` and `AreaItem`s"""
    document = Sections()
    for section in document:
        len(section)
        for item in section:  #pylint:disable=unused-variable
            pass


def test_sections_dump_and_load_sections(restructured_sections_manual):  #pylint:disable=W0621
    data = restructured_sections_manual

    dumped = dump_sections(data)
    assert dumped

    loaded = load_sections(dumped)
    assert loaded

    assert loaded == data


def test_validate_restructured(restructured_sections_manual):  #pylint:disable=W0621
    validated = validate(restructured_sections_manual)
    assert validated


#pylint:disable=W0621
def test_sections_extract_sections_restructured(
        restructured_chapter,
        restructured_index,
        restructured_sections_manual,
        restructured_title,
        restructured_toc,
        restructured_whitepage,
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
    for index, (actual, expected) in enumerate(
            zip(result, restructured_sections_manual)):
        # Compare only the first level
        assert actual.start == expected.start, 'on level: %d' % index
        assert actual.end == expected.end, 'on level: %d' % index

    # TODO: activate later, do not want to make this test so explicit
    # assert result == restructured_sections


def test_sections_chapters(restructured_sections_manual):
    result = chapters(restructured_sections_manual)

    # start is lower or equal than end page size
    # start = item[0]
    # end   = item[1]
    ascending_page_order = all([item[0] <= item[1] for item in result])

    assert ascending_page_order, str([result])
    assert len(result) == 8, str(result)


#pylint:disable=W0621
def test_sections_extract_sections_simple(
        simple_chapter,
        simple_index,
        simple_title,
        simple_toc,
        simple_whitepage,
):
    chapter = load_chapter_detection(simple_chapter)
    index = load_likelihood(simple_index)
    title = load_likelihood(simple_title)
    toc = load_likelihood(simple_toc)
    whitepage = load_whitepages(simple_whitepage)
    whitepage = [whitepage_value_to_percent(item) for item in whitepage]

    source = [chapter, index, title, toc, whitepage]
    result = extract_sections(*source)

    xfail('multiple feature on one page is not solved')


def test_sections_sections_simple(simple_sections):
    xfail('multiple feature on one page is not solved')
