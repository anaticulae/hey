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
