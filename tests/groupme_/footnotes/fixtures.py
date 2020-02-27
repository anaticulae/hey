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

import hey.textnavigator.navigator as htn
import tests.resources


@pytest.fixture
def master72_page14():
    navigators = htn.create_pagetextnavigators_frompath(
        tests.resources.MASTER72,
        pages=(14),
    )
    navigator = utila.select_page(navigators, 14)
    footer = navigator.between(0.8, 0.93)
    assert len(footer) == 7, str(footer)
    return footer


@pytest.fixture
def master89_page7():
    page = 7
    navigators = htn.create_pagetextnavigators_frompath(
        tests.resources.MASTER89,
        pages=(page),
    )
    navigator = utila.select_page(navigators, page)
    footer = navigator.between(0.83, 0.95)
    assert len(footer) == 6, str(footer)
    return footer


@pytest.fixture
def master89_page19():
    page = 19
    navigators = htn.create_pagetextnavigators_frompath(
        tests.resources.MASTER89,
        pages=(page),
    )
    navigator = utila.select_page(navigators, page)
    # TODO: REMOVE WITH EXTRACT MOVING FOOTER
    footer = navigator.between(0.69, 0.95)
    assert len(footer) == 16, len(footer)
    return footer


@pytest.fixture
def bachelor111_page10():
    page = 10
    navigators = htn.create_pagetextnavigators_frompath(
        tests.resources.BACHELOR111,
        pages=(page),
    )
    navigator = utila.select_page(navigators, page)
    # TODO: REMOVE WITH EXTRACT MOVING FOOTER
    footer = navigator.between(0.77, 0.95)
    assert len(footer) == 5, str(footer)
    return footer
