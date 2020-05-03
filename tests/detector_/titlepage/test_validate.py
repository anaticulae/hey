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
import serializeraw

import detector.path
import tests.detector_
import tests.resources


def bachelor76(titlepage: iamraw.TitlePage):
    assert titlepage

    assert titlepage.matrikel.number == 70409886, titlepage.matrikel
    assert titlepage.date.raw == '25.05.2018', titlepage.date
    assert titlepage.thesis.raw == 'Bachelorarbeit', titlepage.thesis.raw

    assert titlepage.author.name == 'Haubrock', titlepage.author
    assert len(titlepage.examiner) == 2, titlepage.examiner


@pytest.mark.parametrize('source, check', [
    pytest.param(tests.resources.BACHELOR76, bachelor76, id='bachelor76'),
])
def test_validate_titlepage_extractor(source, check, testdir, monkeypatch):  #pylint: disable=W0613
    outdir = testdir.tmpdir
    cmd = f'-i {source} -o {outdir} --title --page=0'

    tests.detector_.run(cmd, monkeypatch=monkeypatch)

    path = detector.path.titlepage(outdir)
    titlepage = serializeraw.load_titlepage(path)
    check(titlepage)
