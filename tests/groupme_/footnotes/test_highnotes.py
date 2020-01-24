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


@pytest.fixture
def master89_page_page7():
    page = 7
    navigators = htn.create_pagetextnavigators_frompath(
        tests.resources.MASTER_89PAGES,
        pages=(page),
    )
    navigator = utila.select_page(navigators, page)
    footer = navigator.between(0.83, 0.95)
    assert len(footer) == 6, str(footer)
    return footer


@pytest.fixture
def master89_page_page19():
    page = 19
    navigators = htn.create_pagetextnavigators_frompath(
        tests.resources.MASTER_89PAGES,
        pages=(page),
    )
    navigator = utila.select_page(navigators, page)
    # TODO: REMOVE WITH EXTRACT MOVING FOOTER
    footer = navigator.between(0.7, 0.95)
    assert len(footer) == 16, str(footer)
    return footer


def test_groupme_footnotes_highnotes_split(master72_page14):  # pylint:disable=W0621
    footer = master72_page14
    splitted = list(groupme.footnotes.highnotes.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 7, splitted


def test_groupme_footnotes_highnotes_split_mixed_in_text(master89_page_page7):  # pylint:disable=W0621
    """Test to extract only starting highnotes. In this example, there
    is a highnote inside the text flow."""
    footer = master89_page_page7
    splitted = list(groupme.footnotes.highnotes.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 2, splitted
    merged = groupme.footnotes.highnotes.merge_online(splitted)
    assert len(merged) == 1, merged


def test_groupme_footnotes_highnotes_split_mixed_in_text_tripple(
        master89_page_page19):  # pylint:disable=W0621
    """Test to extract only starting highnotes. In this example, there
    is a highnote inside the text flow and after this there are two more
    footnotes."""
    footer = master89_page_page19
    splitted = list(groupme.footnotes.highnotes.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 4, splitted
    merged = groupme.footnotes.highnotes.merge_online(splitted)
    assert len(merged) == 3, merged

    thirdnote_text = merged[2][1].text
    thirdnote_text = thirdnote_text.strip()  # TODO: REMOVE LATER
    expected = ('Das Schema fasst Vogler (vgl. 21998: 74f.) wie folgt zusammen:'
                ' Der Held wird in seinem Leben in der \ngewohnten Welt '
                'vorgestellt und erh')
    assert thirdnote_text.startswith(expected), thirdnote_text
