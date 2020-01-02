# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw

import hey.textnavigator.navigator
import sections.feature.chapter
import tests.resources


@pytest.mark.parametrize('document, position, toc, expected', [
    pytest.param(
        tests.resources.RESTRUCT_TEXT,
        tests.resources.RESTRUCT_TEXT_POSITION,
        tests.resources.RESTRUCT_TOC,
        [6, 8, 10, 12, 18, 20, 22, 24],
        id='restruct',
    ),
    pytest.param(
        tests.resources.text(tests.resources.MASTER_72PAGES),
        tests.resources.text_positions(tests.resources.MASTER_72PAGES),
        tests.resources.toc(tests.resources.MASTER_72PAGES),
        [3, 6, 22, 45, 63],
        id='master72pages',
    ),
])
def test_sections_chapter_extract(document, position, toc, expected):
    result = extract_chapter(document, position, toc)

    pages = [item.page for item in result]

    assert pages == expected


@pytest.mark.parametrize('document, position, toc', [
    pytest.param(
        tests.resources.RESTRUCT_TEXT,
        tests.resources.RESTRUCT_TEXT_POSITION,
        tests.resources.RESTRUCT_TOC,
        id='restruct',
    ),
])
def test_sections_chapter_dump_and_load_detection(document, position, toc):
    result = extract_chapter(document, position, toc)

    dumped = serializeraw.dump_likelihood(result)
    loaded = serializeraw.load_likelihood(dumped)

    assert loaded == result


def extract_chapter(document, position, toc):
    # load
    document = serializeraw.load_document(document)
    position = serializeraw.load_textpositions(position)
    tocs = serializeraw.load_toc(toc)

    navigators = hey.textnavigator.navigator.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )

    result = sections.feature.chapter.space_between_header_and_first_line(
        navigators,
        tocs,
    )
    return result
