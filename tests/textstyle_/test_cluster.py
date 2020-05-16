# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw
import utila

import tests.resources
import textstyle.cluster
import textstyle.doctextstyle
import textstyle.features
import textstyle.parser
import textstyle.serialize
import textstyle.utils


def navigators(source: str, pages: tuple):
    loaded = serializeraw.create_pagetextnavigators_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    parsed = textstyle.parser.parses(loaded)
    flat = textstyle.utils.flatten(parsed)
    return flat


@pytest.fixture
def master72_text_flat():
    return navigators(
        source=tests.resources.MASTER72,
        pages=tuple(range(3, 86)),
    )


@pytest.fixture
def master72_text_flat_small():
    return navigators(
        source=tests.resources.MASTER72,
        pages=tuple(range(3, 15)),
    )


def test_cluster_size(master72_text_flat):  # pylint:disable=W0621
    data = master72_text_flat
    selection = (textstyle.cluster.ClusterProperty.SIZE,)
    clustered = textstyle.cluster.cluster(data, selection=selection)
    assert len(master72_text_flat) >= 2000
    # six different font size cluster
    assert len(clustered) == 6


def test_cluster_extract_default_textsize(master72_text_flat):  # pylint:disable=W0621
    data = master72_text_flat
    default_text = textstyle.features.text(data)

    # document text size
    assert default_text[0] == 12.0


def test_cluster_extract_pagenumber(master72_text_flat_small):  # pylint:disable=W0621
    pagenumber = textstyle.features.pagenumber(master72_text_flat_small)
    assert pagenumber[0] == 11.04, pagenumber


def test_cluster_extract_headlines_small(master72_text_flat_small):  # pylint:disable=W0621
    headlines = textstyle.features.headlines(
        master72_text_flat_small,
        min_headline_count=3,
    )
    assert len(headlines) == 2
    assert headlines[0][0] == 15.96
    assert headlines[1][0] == 14.04


def test_cluster_extract_headlines_all(master72_text_flat):  # pylint:disable=W0621
    headlines = textstyle.features.headlines(master72_text_flat)
    assert len(headlines) == 3
    assert headlines[0][0] == 15.96, str(headlines)
    assert headlines[1][0] == 14.04, str(headlines)
    assert headlines[2][0] == 12.0, str(headlines)

    headlines = textstyle.features.headlines(
        master72_text_flat,
        returncluster=True,
    )
    assert len(headlines) == 2, str(headlines)


@pytest.mark.parametrize('source, expected', [
    pytest.param(tests.resources.MASTER116, 10.91, id='master116'),
    pytest.param(tests.resources.MASTER98, 12.0, id='master98'),
    pytest.param(tests.resources.MASTER99, 11.04, id='master99'),
    pytest.param(tests.resources.BACHELOR111, 11.96, id='bachelor111'),
])
@utila.skip_longrun
def test_cluster_extract_textsize(source, expected):
    flat = navigators(source, pages=None)
    default_text = textstyle.features.text(flat)
    # document text size
    assert default_text[0] == expected


def test_cluster_extract_footer_small(master72_text_flat_small):  # pylint:disable=W0621
    footnotes = textstyle.features.footnote(master72_text_flat_small)
    fontsize, fontdistance = footnotes[0], footnotes[3]
    assert fontsize == 9.96
    assert fontdistance == (12, 11)


@pytest.mark.parametrize('source, expected', [
    pytest.param(tests.resources.MASTER116, None, id='master116'),
    pytest.param(tests.resources.MASTER98, 9.0, id='master98'),
    pytest.param(tests.resources.MASTER99, 9.0, id='master99'),
    pytest.param(tests.resources.BACHELOR111, 9.96, id='bachelor111'),
])
@utila.skip_longrun
def test_cluster_extract_footnote(source, expected):
    flat = navigators(source, pages=None)
    footnotes = textstyle.features.footnote(flat)
    if expected is None:
        assert footnotes is None
        return
    # document text size
    assert footnotes[0] == expected


def test_cluster_extract_paragraph_small(master72_text_flat_small):  # pylint:disable=W0621
    paragraph = textstyle.features.paragraph(master72_text_flat_small)
    expected = (31, 31)
    assert paragraph == expected, str(paragraph)


@pytest.mark.parametrize('source, expected', [
    pytest.param(tests.resources.MASTER116, (24, 17), id='master116'),
    pytest.param(tests.resources.MASTER98, (41, 41), id='master98'),
    pytest.param(tests.resources.MASTER99, (38, 38), id='master99'),
    pytest.param(tests.resources.BACHELOR111, (24, 24), id='bachelor111'),
])
@utila.skip_longrun
def test_cluster_extract_paragraph(source, expected):
    # TODO: VALIDATE EXPECTED LINE DISTANCE, CURRENTLY THERE ARE NOT
    # CHECKED YET.
    flat = navigators(source, pages=None)
    paragraph = textstyle.features.paragraph(flat)
    assert paragraph == expected


def test_doctextstyle_dump_load():
    source = tests.resources.MASTER98
    result = textstyle.doctextstyle.extract(source)
    assert result

    dumped = textstyle.serialize.dump_docstyle(result)
    loaded = textstyle.serialize.load_docstyle(dumped)
    assert loaded == result
