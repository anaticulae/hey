# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# TODO: Move to iamraw

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
