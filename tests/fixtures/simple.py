# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import serializeraw
import utila

import hey.fonts.store
import hey.textnavigator.navigator
import sections.feature.chapter
import sections.feature.index
import sections.feature.section
import sections.feature.title
import sections.feature.toc
import sections.feature.whitepage
import tests
import tests.fixtures
import tests.resources


@pytest.fixture
def simple():
    pagesize = serializeraw.load_pageborders(tests.resources.SIMPLE_PAGESIZE)
    horizontals = serializeraw.load_horizontals(tests.resources.SIMPLE_HORIZONTAL) # yapf:disable
    position = serializeraw.load_textpositions(tests.resources.SIMPLE_TEXT_POSITION) # yapf:disable
    document = serializeraw.load_document(tests.resources.SIMPLE_TEXT)

    assert pagesize
    assert horizontals
    assert position

    navigator = hey.textnavigator.navigator.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )
    return navigator, horizontals


@pytest.fixture
def simple_document() -> iamraw.Document:
    loaded = serializeraw.load_document(tests.resources.SIMPLE_ONELINE_TEXT)
    return loaded


def simple_document_fixture() -> iamraw.Document:
    loaded = serializeraw.load_document(tests.resources.SIMPLE_TEXT)
    return loaded


def simple_fontstore_fixture() -> hey.fonts.store.FontStore:
    lookup = hey.fonts.store.create_fontstore(
        tests.resources.SIMPLE_FONT_HEADER,
        tests.resources.SIMPLE_FONT_CONTENT,
    )
    return lookup


@pytest.fixture
def simple_fontstore() -> hey.fonts.store.FontStore:
    lookup = hey.fonts.store.create_fontstore(
        tests.resources.SIMPLE_FONT_HEADER,
        tests.resources.SIMPLE_FONT_CONTENT,
    )
    return lookup


@pytest.fixture
def simple_navigator(simple):  #pylint:disable=W0621
    navigator, _ = simple
    return navigator


@pytest.fixture
def simple_pagetextnavigators() -> hey.textnavigator.navigator.PageTextNavigators:  # yapf:disable
    navigator = hey.textnavigator.navigator.create_pagetextnavigators_frompath(
        tests.resources.SIMPLE)
    return navigator


@pytest.fixture
def simple_pagesize():
    size = serializeraw.load_pageborders(tests.resources.SIMPLE_PAGESIZE)
    size = [item.size for item in size]
    return size


@pytest.fixture
def simple_contentborder():
    border = serializeraw.load_pageborders(tests.resources.SIMPLE_PAGESIZE)
    border = [item.border for item in border]
    return border


@pytest.fixture
def simple_page_0(simple_document: iamraw.Document) -> iamraw.Page:  # pylint: disable=W0621
    page: iamraw.Page = simple_document[0]
    return page


@pytest.fixture
def simple_page_2(simple_document: iamraw.Document) -> iamraw.Page:  # pylint: disable=W0621
    page: iamraw.Page = simple_document[2]
    return page


@pytest.fixture
def simple_page_2_text_only(simple_page_2: iamraw.Page):  # pylint: disable=W0621
    lines = []
    for child in simple_page_2:
        if not isinstance(child, iamraw.TextContainer):
            continue
        lines.extend(child.text.splitlines())
    return lines


# TODO: Reduce amout of fixtures
@pytest.fixture
def simple_second_page_navigator(
        simple_pagetextnavigators,  # pylint:disable=W0621
) -> hey.textnavigator.navigator.PageTextNavigator:
    return utila.select_page(simple_pagetextnavigators, page=1)


@pytest.fixture
def simple_second_page_size(simple_contentborder) -> iamraw.Border:  # pylint:disable=W0621
    return simple_contentborder[1]


@pytest.fixture
def simple_toc():
    result = sections.feature.toc.work(tests.resources.SIMPLE_ONELINE_TEXT)
    return result


@pytest.fixture
def simple_whitepage():
    result = sections.feature.whitepage.work(
        tests.resources.SIMPLE_TEXT,
        tests.resources.SIMPLE_TEXT_POSITION,
        tests.resources.SIMPLE_FOOTERS,
    )
    return result


@pytest.fixture
def simple_title():
    result = sections.feature.title.work(
        tests.resources.SIMPLE_ONELINE_TEXT,
        tests.resources.SIMPLE_ONELINE_FONT_HEADER,
        tests.resources.SIMPLE_ONELINE_FONT_CONTENT,
    )
    return result


@pytest.fixture
def simple_index():
    result = sections.feature.index.work(tests.resources.SIMPLE_ONELINE_TEXT)
    return result


@pytest.fixture
def simple_chapter():
    result = sections.feature.chapter.work(
        tests.resources.SIMPLE_TEXT,
        tests.resources.SIMPLE_TEXT_POSITION,
        tests.resources.SIMPLE_TOC,
    )

    # ensure that all chapters are detected
    tests.fixtures.assert_chapter_count(
        serializeraw.load_likelihood(result),
        tests.resources.SIMPLE_CHAPTER_PAGE_COUNT,
    )
    return result


@pytest.fixture
def simple_sections():
    chapter = sections.feature.chapter.work(
        tests.resources.SIMPLE_TEXT,
        tests.resources.SIMPLE_TEXT_POSITION,
        tests.resources.SIMPLE_TOC,
    )

    index = sections.feature.index.work(tests.resources.SIMPLE_TEXT)
    title = sections.feature.title.work(
        tests.resources.SIMPLE_TEXT,
        tests.resources.SIMPLE_FONT_HEADER,
        tests.resources.SIMPLE_FONT_CONTENT,
    )
    toc = sections.feature.toc.work(tests.resources.SIMPLE_TEXT)
    whitepage = sections.feature.whitepage.work(
        tests.resources.SIMPLE_TEXT,
        tests.resources.SIMPLE_TEXT_POSITION,
        tests.resources.SIMPLE_FOOTERS,
    )
    result = sections.feature.section.work(
        chapter,
        index,
        title,
        toc,
        whitepage,
    )
    return result
