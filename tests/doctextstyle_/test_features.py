# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import doctextstyle.features
import tests.doctextstyle_.conftest


def test_cluster_extract_default_textsize(master72_text_flat):
    data = master72_text_flat
    default_text = doctextstyle.features.text(data)

    # document text size
    assert default_text[0] == 12.0


def test_cluster_extract_pagenumber(master72_text_flat_small):
    pagenumber = doctextstyle.features.pagenumber(master72_text_flat_small)
    assert pagenumber[0] == 11.04, pagenumber


def test_cluster_extract_headlines_small(master72_text_flat_small):
    headlines = doctextstyle.features.headlines(
        master72_text_flat_small,
        min_headline_count=3,
    )
    assert len(headlines) == 2
    assert headlines[0][0] == 15.96
    assert headlines[1][0] == 14.04


def test_cluster_extract_headlines_all(master72_text_flat):
    headlines = doctextstyle.features.headlines(master72_text_flat)
    assert len(headlines) == 3
    assert headlines[0][0] == 15.96, str(headlines)
    assert headlines[1][0] == 14.04, str(headlines)
    assert headlines[2][0] == 12.0, str(headlines)

    headlines = doctextstyle.features.headlines(
        master72_text_flat,
        returncluster=True,
    )
    assert len(headlines) == 2, str(headlines)


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.link(power.MASTER116_PDF), 10.91, id='master116'),
    pytest.param(power.link(power.MASTER098_PDF), 12.0, id='master98'),
    pytest.param(power.link(power.MASTER099_PDF), 11.04, id='master99'),
    pytest.param(power.link(power.BACHELOR111_PDF), 11.96, id='bachelor111'),
])
@utilatest.skip_longrun
def test_cluster_extract_textsize(source, expected):
    flat = tests.doctextstyle_.conftest.navigators(source, pages=None)
    default_text = doctextstyle.features.text(flat)
    # document text size
    assert default_text[0] == expected


def test_cluster_extract_footer_small(master72_text_flat_small):
    footnotes = doctextstyle.features.footnote(master72_text_flat_small)
    fontsize, fontdistance = footnotes[0], footnotes[3]
    assert fontsize == 9.96
    assert fontdistance == (11.5, 11.5)


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.link(power.MASTER116_PDF), None, id='master116'),
    pytest.param(power.link(power.MASTER098_PDF), 9.0, id='master98'),
    pytest.param(power.link(power.MASTER099_PDF), 9.0, id='master99'),
    pytest.param(power.link(power.BACHELOR111_PDF), 9.96, id='bachelor111'),
])
@utilatest.skip_longrun
def test_cluster_extract_footnote(source, expected):
    flat = tests.doctextstyle_.conftest.navigators(source, pages=None)
    footnotes = doctextstyle.features.footnote(flat)
    if expected is None:
        assert footnotes is None
        return
    # document text size
    assert footnotes[0] == expected


def test_cluster_extract_paragraph_small(master72_text_flat_small):
    paragraph = doctextstyle.features.paragraph(master72_text_flat_small)
    expected = (31.1, 31.1)
    assert paragraph == expected, str(paragraph)


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.link(power.MASTER116_PDF), (21, 17), id='master116'),
    pytest.param(power.link(power.MASTER098_PDF), (41, 41), id='master98'),
    pytest.param(power.link(power.MASTER099_PDF), (38, 38), id='master99'),
    pytest.param(power.link(power.BACHELOR111_PDF), (24, 24), id='bachelor111'),
])
@utilatest.skip_longrun
def test_cluster_extract_paragraph_before_and_after(source, expected):
    # TODO: VALIDATE EXPECTED LINE DISTANCE, CURRENTLY THERE ARE NOT
    # CHECKED YET.
    flat = tests.doctextstyle_.conftest.navigators(source, pages=None)
    paragraph = doctextstyle.features.paragraph(flat, digits=0)
    assert paragraph == expected
