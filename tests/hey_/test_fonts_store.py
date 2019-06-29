# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# TODO: Move to iamraw

from iamraw import Font
from iamraw import Stretch
from iamraw import Style
from iamraw import Weight
from pytest import fixture
from pytest import mark

from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from tests.resources import RESTRUCT_FONT_CONTENT
from tests.resources import RESTRUCT_FONT_HEADER


@fixture
def restructured_fontstore() -> FontStore:
    lookup = create_fontstore(RESTRUCT_FONT_HEADER, RESTRUCT_FONT_CONTENT)
    return lookup


def restructured_fontstore_fixture() -> FontStore:
    # TODO: Remove with new pytest - this is required, because pytest carn't
    # use fixture in paramertized tests.
    lookup = create_fontstore(RESTRUCT_FONT_HEADER, RESTRUCT_FONT_CONTENT)
    return lookup


@mark.parametrize(
    'page,container,line,char,expected_fontid',
    [
        (0, 0, 1, 5, 0),
        (0, 1, 0, 5, 1),
        (0, 1, 0, 10, 1),
        (0, 2, 0, 11, 2),
        (0, 3, 0, 0, 3),
        (0, 4, 0, 0, None),
        (0, 3, 0, 13, None),
        (0, 3, 1, 0, None),
        (1, 0, 0, 0, None),  # Empty page
        (2, 0, 0, 0, 4),
        (2, 0, 0, 7, 4),
    ])
def test_fontstore_access_font_id(
        restructured_fontstore: FontStore,  # pylint:disable=W0621
        page,
        container,
        line,
        char,
        expected_fontid,
):
    fontstore = restructured_fontstore
    fontid = fontstore.fontid(page, container, line, char)

    assert fontid == expected_fontid


def test_fontstore_from_str(
        restructured_fontstore: FontStore,  # pylint:disable=W0621
):
    """Determine fonts via text input and start of text sequence"""
    fontstore = restructured_fontstore
    text = ('RestructuredText (reST) is a markup language, it’s name coming '
            'from that it’s considered a revision and reinterpreta-\ntion of'
            ' two other markup languages, Setext and StructuredText.')
    first = Font(
        name='OUYNTX+NimbusRomNo9L',
        scale=12.0,
        weight=Weight.LIGHT,
        style=Style.NORMAL,
        stretch=Stretch.REGULAR,
    )
    bold = Font(
        name='DMSGBW+NimbusRomNo9L',
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
    result = fontstore.fromstr(page, 1, 0, text)

    assert len(result) == len(expected), str(result)
    for (res, exp) in zip(result, expected):
        assert res == exp
    assert result == expected, str(result)
