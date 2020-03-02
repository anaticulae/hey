# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import hey.textnavigator.fonts
import tests.resources
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
    distances = hey.textnavigator.fonts.fontdistance(bounds)

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
    bounds = hey.textnavigator.fonts.textbounds(
        simple_second_page_navigator,
        simple_second_page_size,
    )

    assert len(bounds) == len(simple_second_page_navigator)


def test_groupme_fonts_textsize(
        simple_second_page_navigator,  #pylint:disable=W0621
):
    common_size = hey.textnavigator.fonts.textsize_from_page(
        simple_second_page_navigator)
    assert common_size == 9.96


def test_hey_navigator_create_pagetext_navigator_frompath_withfont():
    loaded = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.BACHELOR111,
        pages=(1, 2, 3, 4),
    )
    for page in loaded:
        assert len(page) >= 1
        for line in page:
            assert len(line.style.content) >= 1
            for char in line.style.content:
                # ensure that every char contains font definition
                assert char.font is not None, char
