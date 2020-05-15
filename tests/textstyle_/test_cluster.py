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

import tests.resources
import textstyle.cluster.page
import textstyle.parser
import textstyle.utils


def master116(pages: tuple):
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.MASTER72,
        prefix='oneline',
        pages=pages,
    )
    parsed = textstyle.parser.parses(navigators)
    flat = textstyle.utils.flatten(parsed)
    return flat


@pytest.fixture
def master116_text_flat():
    return master116(pages=tuple(range(3, 86)))


@pytest.fixture
def master116_text_flat_small():
    return master116(pages=tuple(range(3, 15)))


def test_cluster_size(master116_text_flat):  # pylint:disable=W0621
    data = master116_text_flat
    selection = (textstyle.cluster.page.ClusterProperty.SIZE,)
    clustered = textstyle.cluster.page.cluster(data, selection=selection)
    assert len(master116_text_flat) >= 2000
    # six different font size cluster
    assert len(clustered) == 7


def test_cluster_extract_default_textsize(master116_text_flat):  # pylint:disable=W0621
    data = master116_text_flat
    default_text = textstyle.cluster.page.text(data)

    # document text size
    assert default_text[0] == 12.0


def test_cluster_extract_pagenumber(master116_text_flat_small):  # pylint:disable=W0621
    pagenumber = textstyle.cluster.page.pagenumber(master116_text_flat_small)
    assert pagenumber[0] == 11.04, pagenumber


def test_cluster_extract_headlines_small(master116_text_flat_small):  # pylint:disable=W0621
    headlines = textstyle.cluster.page.headlines(master116_text_flat_small)
    assert len(headlines) == 2
    assert headlines[0][0] == 15.96
    assert headlines[1][0] == 14.04


def test_cluster_extract_headlines_all(master116_text_flat):  # pylint:disable=W0621
    headlines = textstyle.cluster.page.headlines(master116_text_flat)
    assert len(headlines) == 3
    assert headlines[0][0] == 15.96, str(headlines)
    assert headlines[1][0] == 14.04, str(headlines)
    assert headlines[2][0] == 12.0, str(headlines)
