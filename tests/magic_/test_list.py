# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila

import tests.magic_


def test_master72_list_multiple_area(testdir, monkeypatch):
    tests.magic_.run(
        (f'-i {power.link(power.MASTER072_PDF, folder="sectionsandwords")} '
         '--pages=8,9,10,11'),
        monkeypatch=monkeypatch,
    )
    loaded = serializeraw.load_types(testdir.tmpdir)

    page9 = utila.select_content(loaded, page=9)
    assert page9
    page9_list = [
        line for line, typ in page9 if typ == iamraw.PageContentType.LIST
    ]
    expected = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    assert page9_list == expected

    page10 = utila.select_content(loaded, page=10)
    assert page10
    page10_list = [
        line for line, typ in page10 if typ == iamraw.PageContentType.LIST
    ]
    expected = [0, 1, 2, 3, 4]
    assert page10_list == expected
