# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw.path
import power
import pytest
import serializeraw
import utila

import groupme.feature.footer
import groupme.footer.strategy as gfs
import groupme.path
import tests.fixtures.restruct
import tests.groupme_
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_pagenumbers
from tests.fixtures.restruct import restructured_pagetextnavigators
from tests.fixtures.restruct import restructured_sizeandborder


def test_groupme_footer_work(testdir):  #pylint:disable=W0621
    root = str(testdir)
    docu27 = power.link(power.DOCU27_PDF)
    dumped = groupme.feature.footer.work(
        iamraw.path.text(docu27),
        iamraw.path.textposition(docu27),
        iamraw.path.fontheader(docu27),
        iamraw.path.fontcontent(docu27),
        iamraw.path.horizontals(docu27),
        iamraw.path.sizeandborder(docu27),
        groupme.path.pagenumbers(docu27),
    )
    assert dumped
    assert len(dumped) > 100, str(dumped)  # there is some content

    utila.file_create(os.path.join(root, 'result.yaml'), dumped)


def test_groupme_footer_dump_and_load(
        restructured_horizontals,  #pylint:disable=W0621
        restructured_sizeandborder,  #pylint:disable=W0621
        restructured_pagenumbers,  #pylint:disable=W0621
        restructured_pagetextnavigators,  #pylint:disable=W0621
):
    horizontals = restructured_horizontals
    pagenumbers = restructured_pagenumbers
    sizeandborders = restructured_sizeandborder
    pagetextnavigators = restructured_pagetextnavigators
    # TODO: use general strategy?
    extracted = gfs.fixed.FixedFooterStrategy(
        horizontals,
        sizeandborders,
        pagenumbers,
        pagetextnavigators,
    )
    extracted = extracted.result()  # pylint:disable=R0204

    dumped = serializeraw.dump_headerfooter(extracted)
    loaded = serializeraw.load_headerfooter(dumped)

    assert loaded == extracted


@pytest.mark.parametrize(
    'strategy, expected_results',
    [
        (gfs.moving.MovingFooterStrategy, 0),
        (gfs.fixed.FixedFooterStrategy, 25),  # TODO: CHECK 25
        (gfs.pages.PageNumberStrategy, 0),
    ])
def test_groupme_footer_footerheader_detectionstategy(
        strategy,
        expected_results,
        restructured_horizontals,  #pylint:disable=W0621
        restructured_sizeandborder,  #pylint:disable=W0621
        restructured_pagenumbers,  #pylint:disable=W0621
        restructured_pagetextnavigators,  # pylint:disable=W0621
):
    """Check that different strategies work proper with given resources

    TODO: SEE DUPLICATION test_footer_judgement_strategy_quality"""
    horizontals = restructured_horizontals
    sizeandborders = restructured_sizeandborder
    pagenumbers = restructured_pagenumbers
    pagetextnavigators = restructured_pagetextnavigators

    process = strategy(
        horizontals=horizontals,
        sizeandborders=sizeandborders,
        pagenumbers=pagenumbers,
        pagetextnavigators=pagetextnavigators,
    )
    result = process.result()
    assert len(result) == expected_results, 'not enough footer and header'


def test_groupme_footer_master72_extract(testdir, monkeypatch):
    outdir = testdir.tmpdir
    cmd = f'-i {power.link(power.MASTER072_PDF)}  -o {outdir} --footer --pages=3'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)

    headfoot = serializeraw.load_headerfooter(iamraw.path.headerfooters(outdir))
    footnotes = headfoot[0].footer.notes
    assert len(footnotes) == 6, str(footnotes)

    first = normalize_whitespaces(footnotes[0].text)
    assert first.startswith('Aus Gründen der besseren Lesbarkeit'), first


def normalize_whitespaces(text: str) -> str:
    text = ' '.join(text.strip().split())
    return text


def test_footer_master98_page10(testdir, monkeypatch):
    cmd = f'-i {power.link(power.MASTER098_PDF)}  --footer --pages=10'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)
    headerpath = iamraw.path.headerfooters(testdir.tmpdir)

    loaded = serializeraw.load_headerfooter(headerpath)
    footer = utila.select_page(loaded, 10).footer
    notes = footer.notes
    assert len(notes) == 1
    firstnote_text = notes[0].text.strip()
    # ensure that page number is not merged to note text
    assert firstnote_text.endswith('16)'), firstnote_text


def test_footer_homework18(testdir, monkeypatch):
    cmd = f'-i {power.link(power.HOMEWORK018_PDF)}  --footer --pages=3:17'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)
    headerpath = iamraw.path.headerfooters(testdir.tmpdir)

    loaded = serializeraw.load_headerfooter(headerpath)
    content = utila.flatten([item.footer.notes for item in loaded])
    # TODO: Change after fixing footnote merger
    assert len(content) == 96, len(content)
    # assert len(content) == 94, len(content)
