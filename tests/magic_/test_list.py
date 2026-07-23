# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import serializeraw
import utilo
import utilotest

import tests.magic_


@utilotest.requires(hoverpower.MASTER072_PDF, folder='sectionsandwords')
def test_master72_list_multiple_area(td, mp):
    source = hoverpower.link(hoverpower.MASTER072_PDF,
                             folder="sectionsandwords")
    pages = '8,9,10,11'
    tests.magic_.run(
        f'-i {source} --pages={pages}',
        mp=mp,
    )
    loaded = serializeraw.load_types(td.tmpdir)
    page9 = utilo.select_content(loaded, page=9)
    assert page9
    page9_list = [
        line for line, typ in page9 if typ == iamraw.PageContentType.LIST
    ]
    expected = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    assert page9_list == expected
    page10 = utilo.select_content(loaded, page=10)
    assert page10
    page10_list = [
        line for line, typ in page10 if typ == iamraw.PageContentType.LIST
    ]
    expected = [0, 1, 2, 3, 4]
    assert page10_list == expected


@utilotest.requires(hoverpower.BACHELOR128_PDF, folder='sectionsandwords')
def test_bachelor128p36_41_list(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR128_PDF,
                             folder="sectionsandwords")
    pages = '36,37,38,39,40,41'
    tests.magic_.run(
        f'-i {source} --pages={pages}',
        mp=mp,
    )
    loaded = serializeraw.load_types(td.tmpdir)
    lists = lambda page: all((item[1] == iamraw.PageContentType.LIST) for item in page) # yapf:disable
    page37 = utilo.select_content(loaded, page=37)
    assert len(page37) == 5
    assert lists(page37)
    page38 = utilo.select_content(loaded, page=38)
    assert len(page38) == 30
    assert lists(page38)
    page39 = utilo.select_content(loaded, page=39)
    assert len(page39) == 11
    assert lists(page39)
