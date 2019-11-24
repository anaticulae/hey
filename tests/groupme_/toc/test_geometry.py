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
    data = bachelor111()

    result = []
    for datum in data:
        parsed = gtsg.analyse_page(datum)
        result.append(parsed)

    first = result[0]
    assert len(first) == 2
    assert len(first[0]) == 3
    assert len(first[1]) == 14

    # second = result[1]
    # print(second)
    # assert len(second) == 4
    # assert len(second[0]) == 2
    # assert len(second[1]) == 8

    # assert len(parsed) == 3
    # for items, expect in zip(result, expected):
    #     assert len(items) == expect
