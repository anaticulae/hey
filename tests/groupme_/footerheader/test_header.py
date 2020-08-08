# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utilatest

import groupme.feature.footer
import groupme.path
import tests.groupme_


@pytest.mark.parametrize('root, expected', [
    pytest.param(
        power.link(power.TECHNICAL_024),
        list(range(1, 24)),
        id='technical24',
    ),
    pytest.param(
        power.link(power.MASTER072_PDF),
        [],
        id='master72',
    ),
])
@utilatest.skip_longrun
def test_groupme_footer_extract_footerheader_technical(root, expected):
    pages = None
    pagetextnavigators = serializeraw.create_pagetextnavigators_frompath(
        root,
        pages=pages,
    )

    horizontals = serializeraw.load_horizontals(
        iamraw.path.horizontals(root),
        pages=pages,
    )

    sizeandborders = serializeraw.load_pageborders(
        iamraw.path.sizeandborder(root),
        pages=pages,
    )

    pagenumbers = serializeraw.load_pagenumbers(
        groupme.path.pagenumbers(root),
        pages=pages,
    )

    result = groupme.feature.footer.extract_footerheader(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )

    header = [item.page for item in result if item.header is not None]
    assert header == expected


def test_groupme_header_bachelor90(testdir, monkeypatch):
    cmd = f'-i {power.link(power.BACHELOR090_PDF)}  --footer --pages=11:24'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)
    headerpath = iamraw.path.headerfooters(testdir.tmpdir)

    loaded = serializeraw.load_headerfooter(headerpath)
    header = [item.header for item in loaded if item.header]
    assert len(header) == 11


def test_groupme_header_bachelor37_starting_index(testdir, monkeypatch):
    """Ensure that parts of pages `4:14` for example are indexed correctly."""
    cmd = f'-i {power.link(power.BACHELOR037_PDF)}  --footer --pages=4:14'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)
    headerpath = iamraw.path.headerfooters(testdir.tmpdir)

    loaded = serializeraw.load_headerfooter(headerpath)
    assert loaded[0].header.page.value == 4


def test_groupme_header_bachelor37_all(testdir, monkeypatch):
    cmd = f'-i {power.link(power.BACHELOR037_PDF)}  --footer'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)
    headerpath = iamraw.path.headerfooters(testdir.tmpdir)

    loaded = serializeraw.load_headerfooter(headerpath)
    header = [item.header for item in loaded if item.header]

    noheader = [0, 5, 33]
    expected = [item for item in range(0, 37) if item not in noheader]
    current = [item.page.value for item in header]
    assert current == expected
