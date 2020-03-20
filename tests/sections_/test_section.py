# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw

import sections.creator
import sections.feature.section
import tests.resources
import tests.sections_
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


def test_section_iterable():
    """Create empty `Sections` and iterate over `Sections` and `AreaItem`s"""
    document = iamraw.Sections()
    for section in document:
        len(section)
        for item in section:  #pylint:disable=unused-variable
            pass


def test_section_dump_and_load_sections(restructured_sections_manual):  #pylint:disable=W0621
    data = restructured_sections_manual

    dumped = serializeraw.dump_sections(data)
    assert dumped

    loaded = serializeraw.load_sections(dumped)
    assert loaded

    assert loaded == data


def test_section_validate_restructured(restructured_sections_manual):  #pylint:disable=W0621
    validated = sections.creator.validate(restructured_sections_manual)
    assert validated


#pylint:disable=W0621
def test_section_extract_sections_restructured(
        testdir,
        monkeypatch,
        restructured_sections_manual,
):
    root = testdir.tmpdir
    source = tests.resources.RESTRUCT
    tests.sections_.run_sections(f'-i {source}', monkeypatch=monkeypatch)

    result = sections.feature.section.load_section_likelihood_frompath(root)
    assert result
    for index, (actual, expected) in enumerate(
            zip(result, restructured_sections_manual)):
        # Compare only the first level
        assert actual.start == expected.start, 'on level: %d' % index
        assert actual.end == expected.end, 'on level: %d' % index

    # TODO: activate later, do not want to make this test so explicit
    # assert result == restructured_sections


def test_section_chapters(restructured_sections_manual):
    result = sections.feature.section.chapters(restructured_sections_manual)

    # start is lower or equal than end page size
    # start = item[0]
    # end   = item[1]
    ascending_page_order = all([item[0] <= item[1] for item in result])

    assert ascending_page_order, str([result])
    assert len(result) == 8, str(result)


#pylint:disable=W0621
def test_section_extract_sections_simple():
    result = sections.feature.section.extract_sections_frompath(
        tests.resources.HOWTO_PYPORTING)

    expected = [
        iamraw.MultipleSection,
        iamraw.MainPart,
    ]

    assert len(result) == len(expected), 'wrong area split'
    for current, wanted in zip(result, expected):
        current = current.__class__.__name__
        wanted = wanted.__name__
        assert current == wanted, f'{current} != {wanted}'

    # Title and Table of MultipleSection
    assert len(result[0].content) == 2

    # TODO: Test order of multiple items


def test_section_sections_simple(simple_sections):
    """Check dumped result of section work method"""
    assert len(simple_sections) == 2, len(simple_sections)
    dumped = serializeraw.dump_sections(simple_sections)
    assert len(dumped) > 100, dumped
    loaded = serializeraw.load_sections(dumped)
    assert loaded == simple_sections, loaded
