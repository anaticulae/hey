# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import groupme.toc.strategy.geometry as gtsg
import hey.textnavigator.navigator as htn
import tests.resources


def master72() -> htn.PageTextNavigators:
    result = htn.create_pagetextnavigators_frompath(
        tests.resources.MASTER_72PAGES,
        pages=(1, 2),
        prefix='oneline',
    )
    return result


def bachelor111():
    result = htn.create_pagetextcontentnavigators_frompath(
        tests.resources.BACHELOR_111PAGES,
        pages=(1, 2, 3, 4),
        prefix='oneline',
    )
    return result


def test_groupme_toc_geometry_analyse_page_master72():
    data = master72()

    firstpage = data[0]
    parsed = gtsg.analyse_page(firstpage)
    assert len(parsed) == 3

    secondpage = data[1]
    parsed = gtsg.analyse_page(secondpage)
    assert len(parsed) == 4


def test_groupme_toc_geometry_analyse_page_bachelor111():
    """Check that geometry approach parses and group toc lines correctly."""

    expected = [
        [3, 14],  # first toc page
        [2, 8, 5, 6],
        [1, 8, 3, 1, 4, 1, 1, 1],
        [9],  # last toc page with appendix group
    ]
    data = bachelor111()

    result = [gtsg.analyse_page(item) for item in data]

    current = [[len(item) for item in group] for group in result]

    assert current == expected
