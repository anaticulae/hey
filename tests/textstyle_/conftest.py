# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw

import tests.resources
import textstyle.parser
import textstyle.utils


def navigators(source: str, pages: tuple):
    loaded = serializeraw.create_pagetextnavigators_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    parsed = textstyle.parser.parses(loaded)
    flat = textstyle.utils.flatten(parsed)
    return flat


@pytest.fixture
def master72_text_flat():
    return navigators(
        source=tests.resources.MASTER72,
        pages=tuple(range(3, 86)),
    )


@pytest.fixture
def master72_text_flat_small():
    return navigators(
        source=tests.resources.MASTER72,
        pages=tuple(range(3, 15)),
    )
