# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_toc

from groupme.feature.numbers import load_textposition
from hey.textnavigator.navigator import create_pagetextnavigator
from sections.feature.chapter import dump_chapter_detection
from sections.feature.chapter import load_chapter_detection
from sections.feature.chapter import space_between_header_and_first_line
from sections.feature.chapter import work
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TEXT_POSITION
from tests.resources import RESTRUCT_TOC


# def space_between_header_and_first_line(
#         document: Document,
#         navigators: List[PageTextNavigator],
#         headerfooters,
# ):
def test_chapter_extract():
    # load
    document = load_document(RESTRUCT_TEXT)
    position = load_textposition(RESTRUCT_TEXT_POSITION)
    tocs = load_toc(RESTRUCT_TOC)
    # TODO: Think about how to handle this, invocation order of features?
    navigators = create_pagetextnavigator(position, document)

    result = space_between_header_and_first_line(
        navigators,
        tocs,
    )

    expected = [
        False,
        False,
        False,
        False,
        False,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        False,
        False,
        False,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        False,
    ]

    selected = [item > 0.0 for item in result]

    assert selected == expected


def test_chapter_dump_and_load_detection():
    # load
    document = load_document(RESTRUCT_TEXT)
    position = load_textposition(RESTRUCT_TEXT_POSITION)
    tocs = load_toc(RESTRUCT_TOC)
    # TODO: Think about how to handle this, invocation order of features?
    navigators = create_pagetextnavigator(position, document)

    result = space_between_header_and_first_line(
        navigators,
        tocs,
    )

    dumped = dump_chapter_detection(result)
    loaded = load_chapter_detection(dumped)

    assert loaded == result


@fixture
def restructured_chapter():
    result = work(RESTRUCT_TEXT, RESTRUCT_TEXT_POSITION, RESTRUCT_TOC)
    return result
