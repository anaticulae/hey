# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw import Border
from iamraw import Document
from iamraw import Page
from iamraw import TextContainer
from pytest import fixture
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_pageborders

from groupme.feature.numbers import load_textposition
from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import PageTextNavigators
from hey.textnavigator.navigator import create_pagetextnavigators
from tests.resources import SIMPLE_FONT_CONTENT
from tests.resources import SIMPLE_FONT_HEADER
from tests.resources import SIMPLE_HORIZONTAL
from tests.resources import SIMPLE_PAGESIZE
from tests.resources import SIMPLE_POSITION
from tests.resources import SIMPLE_TEXT


@fixture
def simple():
    pagesize = load_pageborders(SIMPLE_PAGESIZE)
    horizontals = load_horizontals(SIMPLE_HORIZONTAL)
    position = load_textposition(SIMPLE_POSITION)
    document = load_document(SIMPLE_TEXT)

    assert pagesize
    assert horizontals
    assert position

    assert len(position) == len(document)
    assert len(horizontals) == len(document)

    navigator = create_pagetextnavigators(position, document)
    return navigator, horizontals


@fixture
def simple_document() -> Document:
    loaded = load_document(SIMPLE_TEXT)
    return loaded


def simple_document_fixture() -> Document:
    loaded = load_document(SIMPLE_TEXT)
    return loaded


def simple_fontstore_fixture() -> FontStore:
    lookup = create_fontstore(SIMPLE_FONT_HEADER, SIMPLE_FONT_CONTENT)
    return lookup


@fixture
def simple_fontstore() -> FontStore:
    lookup = create_fontstore(SIMPLE_FONT_HEADER, SIMPLE_FONT_CONTENT)
    return lookup


@fixture
def simple_navigator(simple):  #pylint:disable=W0621
    navigator, _ = simple
    return navigator


@fixture
def simple_pagetextnavigators(
        simple_document: Document,  #pylint:disable=W0621
) -> PageTextNavigators:
    textpositions = load_textposition(SIMPLE_POSITION)

    return create_pagetextnavigators(textpositions, simple_document)


@fixture
def simple_pagesize():
    size, _ = load_pageborders(SIMPLE_PAGESIZE)
    return size


@fixture
def simple_contentborder():
    _, border = load_pageborders(SIMPLE_PAGESIZE)
    return border


@fixture
def simple_page_0(simple_document: Document) -> Page:  # pylint: disable=W0621
    page: Page = simple_document[0]
    return page


@fixture
def simple_page_2(simple_document: Document) -> Page:  # pylint: disable=W0621
    page: Page = simple_document[2]
    return page


@fixture
def simple_page_2_text_only(simple_page_2: Page):  # pylint: disable=W0621
    lines = []
    for child in simple_page_2:
        if not isinstance(child, TextContainer):
            continue
        lines.extend(child.text.splitlines())
    return lines


# TODO: Reduce amout of fixtures
@fixture
def simple_second_page_navigator(
        simple_pagetextnavigators) -> PageTextNavigator:
    return simple_pagetextnavigators[1]


@fixture
def simple_second_page_size(simple_contentborder) -> Border:
    return simple_contentborder[1]
