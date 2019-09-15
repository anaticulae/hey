# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
from serializeraw import load_document
from serializeraw import load_toc

from groupme.feature.numbers import load_textposition
from hey.textnavigator.navigator import create_pagetextnavigators
from sections.feature.chapter import space_between_header_and_first_line
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TEXT_POSITION
from tests.resources import RESTRUCT_TOC


def test_chapter_extract():
    document = load_document(RESTRUCT_TEXT)
    position = load_textposition(RESTRUCT_TEXT_POSITION)
    tocs = load_toc(RESTRUCT_TOC)

    navigators = create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    result = space_between_header_and_first_line(
        navigators,
        tocs,
    )

    expected = [6, 8, 10, 12, 18, 20, 22, 24]

    pages = [item.page for item in result]

    assert pages == expected


def test_chapter_dump_and_load_detection():
    # load
    document = load_document(RESTRUCT_TEXT)
    position = load_textposition(RESTRUCT_TEXT_POSITION)
    tocs = load_toc(RESTRUCT_TOC)
    # TODO: Think about how to handle this, invocation order of features?
    navigators = create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    result = space_between_header_and_first_line(
        navigators,
        tocs,
    )

    dumped = serializeraw.dump_likelihood(result)
    loaded = serializeraw.load_likelihood(dumped)

    assert loaded == result
