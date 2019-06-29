# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import mark
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
from tests.fixtures.restruct import restructured_sections
from tests.fixtures.restruct import restructured_title
from tests.fixtures.restruct import restructured_toc
from tests.fixtures.restruct import restructured_whitepage


def test_sections_iterable():
    """Create empty `Sections` and iterate over `Sections` and `AreaItem`s"""
    document = Sections()
    for section in document:
        len(section)
        for item in section:  #pylint:disable=unused-variable
            pass


@mark.xfail(reason='not fully implemented')
def test_sections_dump_and_load_sections(restructured_sections):  #pylint:disable=W0621
    data = restructured_sections

    dumped = dump_sections(data)
    assert dumped

    loaded = load_sections(dumped)
    assert loaded

    assert loaded == data


def test_validate_restructured(restructured_sections):  #pylint:disable=W0621
    validated = validate(restructured_sections)
    assert validated


#pylint:disable=W0621
def test_sections_extract_sections(
        restructured_chapter,
        restructured_index,
        restructured_sections,
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
            zip(result, restructured_sections)):
        print('check level %d' % index)
        # Compare only the first level
        assert actual.start == expected.start
        assert actual.end == expected.end

    # TODO: activate later, do not want to make this test so explicit
    # assert result == restructured_sections


def test_sections_chapters(restructured_sections):
    result = chapters(restructured_sections)

    # start is lower or equal than end page size
    # start = item[0]
    # end   = item[1]
    ascending_page_order = all([item[0] <= item[1] for item in result])

    assert ascending_page_order, str([result])
    assert len(result) == 8, str(result)
