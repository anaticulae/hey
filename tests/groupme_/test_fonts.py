# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw import Border
from pytest import fixture

from groupme.textnavigator.fonts import fontdistance
from groupme.textnavigator.fonts import fontsizes
from groupme.textnavigator.fonts import textbounds
from groupme.textnavigator.fonts import textsize
from groupme.textnavigator.navigator import PageTextNavigator
from tests.resources import simplecontentborder
from tests.resources import simpledocument
from tests.resources import simplepagetextnavigators


@fixture
def simple_second_page_navigator(simplepagetextnavigators) -> PageTextNavigator:
    return simplepagetextnavigators[1]


@fixture
def simple_second_page_size(simplecontentborder) -> Border:
    return simplecontentborder[1]


def test_groupme_fonts_fondistance(simple_second_page_navigator):
    # if you have 3 item, you have 2 distances A -> B, B-> C
    distance_count = len(list(simple_second_page_navigator)) - 1

    distances = fontdistance(simple_second_page_navigator)

    assert len(distances) == distance_count

    ### 2 elements with negative font size, cause there matching together

    # 6. Use caniusepython3 to find out which
    #    (pip install caniusepython3)
    # 7. Once your dependencies are no lonns
    #    ...
    #    tox)

    negative_distance = [item for item in distances if item < 0.0]
    assert len(negative_distance) == 2


def test_groupme_fonts_textbounds(
        simple_second_page_navigator,
        simple_second_page_size,
):
    bounds = textbounds(simple_second_page_navigator, simple_second_page_size)

    assert len(bounds) == len(simple_second_page_navigator)


def test_groupme_fonts_textsize(
        simple_second_page_navigator,
        simple_second_page_size,
):
    bounds = textbounds(simple_second_page_navigator, simple_second_page_size)

    sizes = fontsizes(bounds)

    common_size = textsize(sizes)

    assert common_size == 13
