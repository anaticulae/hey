# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw

import doctextstyle.parser
import doctextstyle.utils


@pytest.fixture
def master116_text():
    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.MASTER072_PDF),
        prefix='oneline',
        pages=(3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
    )
    return navigators


def test_textstyle_parse_page(master116_text):  # pylint:disable=W0621
    parsed = doctextstyle.parser.parses(master116_text)
    assert len(parsed) == len(master116_text)


def test_flatten_textproperties(master116_text):  # pylint:disable=W0621
    parsed = doctextstyle.parser.parses(master116_text)
    flat = doctextstyle.utils.flatten(parsed)
    assert len(flat) >= len(master116_text) * 5
