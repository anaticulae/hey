# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import groupme.footnotes.highnotes
import hey.textnavigator.navigator as htn
import tests.resources


@pytest.fixture
def master72_page14():
    navigators = htn.create_pagetextnavigators_frompath(
        tests.resources.MASTER_72PAGES,
        pages=(14),
    )
    navigator = utila.select_page(navigators, 14)
    footer = navigator.between(0.8, 0.93)
    assert len(footer) == 7, str(footer)
    return footer


def test_groupme_footnotes_highnotes_split(master72_page14):  # pylint:disable=W0621
    footer = master72_page14
    splitted = list(groupme.footnotes.highnotes.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 7, splitted
