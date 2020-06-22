# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import texmex
import utilatest

import groupme.footnotes.highnotes
import groupme.footnotes.parser
# pylint:disable=W0611
from tests.groupme_.footnotes.fixtures import bachelor111_page10
from tests.groupme_.footnotes.fixtures import master72_page14
from tests.groupme_.footnotes.fixtures import master89_page7
from tests.groupme_.footnotes.fixtures import master89_page19


@utilatest.skip_longrun
def test_groupme_footnote_highnotes_split(master72_page14):  # pylint:disable=W0621
    footer = master72_page14
    splitted = list(groupme.footnotes.highnotes.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 7, splitted


@utilatest.skip_longrun
def test_groupme_footnote_highnotes_split_mixed_in_text(master89_page7):  # pylint:disable=W0621
    """Test to extract only starting highnotes. In this example, there
    is a highnote inside the text flow."""
    footer = master89_page7
    splitted = list(groupme.footnotes.highnotes.split_textinfo(footer))
    assert splitted, splitted
    assert len(splitted) == 2, splitted
    merged = groupme.footnotes.highnotes.merge_online(splitted)
    assert len(merged) == 1, merged


@utilatest.skip_longrun
def test_groupme_footnote_highnotes_split_mixed_in_text_tripple(
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


@utilatest.skip_longrun
def test_groupme_footnote_parse_footer_with_highnotes(master89_page7):  # pylint:disable=W0621
    parsed = groupme.footnotes.parser.parse_with_highnotes(master89_page7)
    assert len(parsed) == 1, parsed


def test_groupme_footnote_highnotes_oneline_with_intention(bachelor111_page10):  # pylint:disable=W0621,W0613
    parsed = groupme.footnotes.parser.parse_with_highnotes(bachelor111_page10)
    assert len(parsed) == 3, str(parsed)
    notes = [item.number for item in parsed]
    assert notes == [3, 4, 5], str(notes)


# yapf:disable
ITEMS = [
    texmex.TextInfo(**{
        'text':'8Data Length Code\n',
        'bounding':iamraw.BoundingBox(x0=86.85, y0=623.17, x1=171.64, y1=636.74),
        'style':texmex.TextStyle(content=[
            texmex.CharStyle(start=0, end=1, size=7.57, rise=4.29, font=773298602),
            texmex.CharStyle(start=1, end=18, size=9.96, rise=0.0, font=904427114)
        ]),
        'bounding_mean':12.01,
        },),
    texmex.TextInfo(**{
        'text':'9\n',
        'bounding':iamraw.BoundingBox(x0=86.85, y0=635.54, x1=90.64, y1=644.82),
        'style':texmex.TextStyle(content=[
            texmex.CharStyle(start=0, end=2, size=7.57, rise=0.0, font=773298602)
        ]),
        'bounding_mean':9.28,
        },),
    texmex.TextInfo(**{
        'text':'„Die Hamming-Distanz d(C) eines Codes C gibt den minimalen Abstand zwischen zwei gültigen,\n',
        'bounding':iamraw.BoundingBox(x0=91.14, y0=636.88, x1=514.1, y1=655.01),
        'style':texmex.TextStyle(content=[
            texmex.CharStyle(start=0, end=1, size=9.96, rise=0.0, font=904427114),
            texmex.CharStyle(start=1, end=84, size=9.96, rise=5.9, font=904427114),
            texmex.CharStyle(start=84, end=85, size=9.96, rise=5.92, font=904427114),
            texmex.CharStyle(start=85, end=93, size=9.96, rise=5.9, font=904427114)
        ]),
        'bounding_mean':12.21,
        },),
]
#yapf:enable

EXPECTED = [
    'Data Length Code',
    '”Die Hamming-Distanz d(C) eines Codes C gibt den minimalen Abstand zwischen zwei gültigen',
]


@pytest.mark.xfail(reason='bad formatted pdf file')
def test_highnotes_prepare():
    # TODO: WE HAVE TO FIX THIS LATER. IT IS A LITTLE BIT COMPLICATED,
    # CAUSE HIGHNOTE/TEXT IS NOT PRINTED CORRECTLY, THEREFORE WE MAY
    # REQUIRE A NEW PARSING STRATEGY.
    parsed = groupme.footnotes.parser.parse_with_highnotes(ITEMS)
    lines = [item.text for item in parsed]
    assert lines == EXPECTED
