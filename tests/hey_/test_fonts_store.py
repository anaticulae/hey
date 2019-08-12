# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# TODO: Move to iamraw

from iamraw import Document
from iamraw import Font
from iamraw import PageFontContent
from iamraw import Stretch
from iamraw import Style
from iamraw import Weight
from pytest import fixture
from pytest import mark

from groupme.feature.numbers import load_textposition
from hey.fonts.store import NO_FONT
from hey.fonts.store import FontContentStore
from hey.fonts.store import FontStore
from hey.textnavigator.navigator import PageTextContentNavigator
from hey.textnavigator.navigator import PageTextNavigators
from hey.textnavigator.navigator import create_pagetextnavigators
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_border
from tests.fixtures.restruct import restructured_contentborder
from tests.fixtures.restruct import restructured_fontstore
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_text
from tests.resources import RESTRUCT_PAGESIZE
from tests.resources import RESTRUCT_TEXT_POSITION
from words.feature.headlines import content_border

FIRST_FONT = Font(
    name='NimbusSanL',
    scale=31.1,
    weight=Weight.BOLD,
)

SECOND_FONT = Font(
    name='NimbusSanL',
    scale=21.7,
    weight=Weight.BOLD,
    style=Style.ITALIC,
)
THIRD_FONT = Font(
    name='NimbusSanL',
    scale=21.6,
    weight=Weight.BOLD,
)

FORTH_FONT = Font(
    name='NimbusSanL',
    scale=15.0,
    weight=Weight.BOLD,
)

FIFTH_FONT = Font(
    name='NimbusSanL',
    scale=17.8,
    weight=Weight.LIGHT,
    style=Style.NORMAL,
    stretch=Stretch.REGULAR,
)


@mark.parametrize(
    'page,container,line,char,expected',
    [
        (0, 0, 1, 5, FIRST_FONT),
        (0, 1, 0, 5, SECOND_FONT),
        (0, 1, 0, 10, SECOND_FONT),
        (0, 2, 0, 11, THIRD_FONT),
        (0, 3, 0, 0, FORTH_FONT),
        (0, 4, 0, 0, NO_FONT),
        (0, 3, 0, 13, NO_FONT),
        (0, 3, 1, 0, NO_FONT),
        (1, 0, 0, 0, NO_FONT),  # Empty page
        (2, 0, 0, 0, FIFTH_FONT),
        (2, 0, 0, 7, FIFTH_FONT),
    ])  #TODO: THINK ABOUT BETTER APPRAOCH THAN SAVING HASH KEY
def test_fontstore_access_font_id(
        restructured_fontstore: FontStore,  # pylint:disable=W0621
        page,
        container,
        line,
        char,
        expected,
):
    expected_fontid = hash(expected)
    fontstore = restructured_fontstore
    fontid = fontstore.fontid(page, container, line, char)
    if expected == NO_FONT:
        expected_fontid = NO_FONT
    assert fontid == expected_fontid


def expected_result():
    text = ('RestructuredText (reST) is a markup language, it’s name coming '
            'from that it’s considered a revision and reinterpreta-\ntion of'
            ' two other markup languages, Setext and StructuredText.')
    first = Font(
        name='NimbusRomNo9L',
        scale=12.0,
        weight=Weight.LIGHT,
        style=Style.NORMAL,
        stretch=Stretch.REGULAR,
    )
    bold = Font(
        name='NimbusRomNo9L',
        scale=13.0,
        weight=Weight.MEDIUM,
        style=Style.NORMAL,
        stretch=Stretch.REGULAR,
    )
    expected = [
        (text[0:154], first),
        (text[154:161], bold),
        (text[161:165], first),
        (text[165:179], bold),
        (text[179:], first),
    ]
    page = 4

    return (text, page, expected)


def test_fontstore_from_str(
        restructured_fontstore: FontStore,  # pylint:disable=W0621
):
    """Determine fonts via text input and start of text sequence"""
    fontstore = restructured_fontstore
    (text, page, expected) = expected_result()
    result = fontstore.fromstr(page, 1, 0, text)

    assert len(result) == len(expected), str(result)
    for (res, exp) in zip(result, expected):
        assert res == exp
    assert result == expected, str(result)


@fixture
def restructured_textnavigators(restructured_text: Document,
                               ) -> PageTextNavigators:
    textpositions = load_textposition(RESTRUCT_TEXT_POSITION)
    return create_pagetextnavigators(
        text=restructured_text,
        text_position=textpositions,
    )


@fixture
def restructured_pagetextcontentnavigator(
        restructured_textnavigators,
        restructured_contentborder,
) -> PageTextContentNavigator:
    # page_1 = res[1]
    # pagetextnavigator: PageTextNavigators(),
    contentborders = restructured_contentborder
    page = 4
    navigator = restructured_textnavigators[page]
    pagecontent = PageTextContentNavigator(
        navigator,
        contentborders,
    )
    return pagecontent


def test_fontstore_fontcontentstore(
        restructured_pagetextcontentnavigator,
        restructured_fontstore,
):
    navigator = restructured_pagetextcontentnavigator
    fontstore = restructured_fontstore
    content = FontContentStore(
        store=fontstore,
        navigator=navigator,
        page=4,
    )
    (text, _, expected) = expected_result()
    result = content.fromstr(0, 0, text)

    assert len(result) == len(expected), str(result)
    for (res, exp) in zip(result, expected):
        assert res == exp
    assert result == expected, str(result)


def test_fontstore_font_to_fontid():
    # prepare sample font store
    # pylint:disable=C0103
    f0 = Font(name='SuperFont', scale=12.5)
    f1 = Font(name='Arial', scale=12.5)
    f2 = Font(name='Verdana', scale=17.5)
    f3 = Font(name='Times', scale=5)
    f4 = Font(name='Arial', scale=20)
    f5 = Font(name='Arial', scale=5)
    header = [f0, f1, f2, f3, f4, f5]
    content = [PageFontContent(content=[], page=0)]

    store = FontStore(header, content)
    assert store.font_to_fontid(f4) == hash(f4)
    assert store.font_to_fontid(f3) == hash(f3)
    assert store.font_to_fontid(f3) == hash(f3)
    assert store.font_to_fontid(f0) == hash(f0)
    assert store.font_to_fontid(f5) == hash(f5)
