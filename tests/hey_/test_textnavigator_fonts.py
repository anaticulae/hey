# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from hey.textnavigator.fonts import fontdistance
from hey.textnavigator.fonts import textbounds
from hey.textnavigator.fonts import textsize_from_page
#pylint:disable=W0611
from tests.fixtures.simple import simple_contentborder
from tests.fixtures.simple import simple_document
from tests.fixtures.simple import simple_pagetextnavigators
from tests.fixtures.simple import simple_second_page_navigator
from tests.fixtures.simple import simple_second_page_size


def test_groupme_fonts_fontdistance(simple_second_page_navigator):  #pylint:disable=W0621
    content = simple_second_page_navigator
    # if you have 3 item, you have 2 distances A -> B, B-> C
    distance_count = len(content) - 1
    bounds = [item.bounding for item in content]
    distances = fontdistance(bounds)

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
        simple_second_page_navigator,  #pylint:disable=W0621
        simple_second_page_size,  #pylint:disable=W0621
):
    bounds = textbounds(simple_second_page_navigator, simple_second_page_size)

    assert len(bounds) == len(simple_second_page_navigator)


def test_groupme_fonts_textsize(
        simple_second_page_navigator,  #pylint:disable=W0621
):
    common_size = textsize_from_page(simple_second_page_navigator)
    assert common_size == 9.96
