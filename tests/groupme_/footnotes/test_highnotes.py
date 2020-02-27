# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import groupme.footnotes.highnotes
import groupme.footnotes.parser
# pylint:disable=W0611
from tests.groupme_.footnotes.fixtures import bachelor111_page10
from tests.groupme_.footnotes.fixtures import master72_page14
from tests.groupme_.footnotes.fixtures import master89_page7
from tests.groupme_.footnotes.fixtures import master89_page19


@utila.skip_longrun
def test_groupme_footnotes_highnotes_split(master72_page14):  # pylint:disable=W0621
    footer = master72_page14
    splitted = list(groupme.footnotes.highnotes.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 7, splitted


@utila.skip_longrun
def test_groupme_footnotes_highnotes_split_mixed_in_text(master89_page7):  # pylint:disable=W0621
    """Test to extract only starting highnotes. In this example, there
    is a highnote inside the text flow."""
    footer = master89_page7
    splitted = list(groupme.footnotes.highnotes.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 2, splitted
    merged = groupme.footnotes.highnotes.merge_online(splitted)
    assert len(merged) == 1, merged


@utila.skip_longrun
def test_groupme_footnotes_highnotes_split_mixed_in_text_tripple(
        master89_page19):  # pylint:disable=W0621
    """Test to extract only starting highnotes. In this example, there
    is a highnote inside the text flow and after this there are two more
    footnotes."""
    footer = master89_page19
    splitted = list(groupme.footnotes.highnotes.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 4, splitted
    merged = groupme.footnotes.highnotes.merge_online(splitted)
    assert len(merged) == 3, merged

    thirdnote_text = merged[2][1].text
    thirdnote_text = thirdnote_text.strip()  # TODO: REMOVE LATER
    expected = ('Das Schema fasst Vogler (vgl. 21998: 74f.) wie folgt zusammen:'
                ' Der Held wird in seinem Leben in der\ngewohnten Welt '
                'vorgestellt und erh')
    assert thirdnote_text.startswith(expected), thirdnote_text


@utila.skip_longrun
def test_groupme_footnotes_parse_footer_with_highnotes(master89_page7):  # pylint:disable=W0621
    parsed = groupme.footnotes.parser.parse_with_highnotes(master89_page7)
    assert len(parsed) == 1, parsed


@utila.skip_longrun
def test_groupme_footnotes_highnotes_oneline_with_intention(bachelor111_page10):  # pylint:disable=W0621,W0613
    # TODO: add test that highnotes are on oneline!
    # CHECK Intentation, must be near 0.0
    pass
