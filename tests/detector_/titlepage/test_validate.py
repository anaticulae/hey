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
import utila

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


def master98(titlepage: iamraw.TitlePage):
    assert titlepage
    assert len(titlepage.examiner) == 2, titlepage.examiner
    assert titlepage.institution, titlepage.institution
    assert titlepage.thesis.typ == iamraw.DocumentType.MASTER, titlepage.thesis
    assert titlepage.date, titlepage.date


def bachelor241(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.thesis.typ == iamraw.DocumentType.BACHELOR
    assert titlepage.title == (
        'SOLAR II - Komplexe Modellierung von beruﬂichen '
        'Allergierisiken und Simulation zur Anwendung von Imputationsmethoden')
    assert len(titlepage.examiner) == 3, titlepage.examiner


def master78(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.matrikel.number == 1024577
    assert len(titlepage.examiner) == 2
    assert titlepage.title == (
        'Entwicklung eines Softwaresystems zur Planung'
        ' und Inbetriebnahme von Gebäudeautomationssystemen')


def homework50(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.thesis.typ == iamraw.DocumentType.STUDY
    assert titlepage.title == 'Implementierung eines Leistungsmesssystem auf dem MSP430'
    assert len(titlepage.examiner) == 3, titlepage.examiner


@pytest.mark.parametrize('source, check', [
    pytest.param(tests.resources.BACHELOR76, bachelor76, id='bachelor76'),
    pytest.param(tests.resources.MASTER98, master98, id='master98'),
    pytest.param(
        tests.resources.BACHELOR241,
        bachelor241,
        id='bachelor241',
        marks=pytest.mark.xfail(reason='improve headline parser'),
    ),
    pytest.param(
        tests.resources.MASTER78,
        master78,
        id='master78',
        marks=pytest.mark.xfail(reason='improve headline parser'),
    ),
    pytest.param(
        tests.resources.HOMEWORK50,
        homework50,
        id='homework50',
        marks=pytest.mark.xfail(reason='improve headline parser'),
    ),
])
@utila.skip_longrun
def test_validate_titlepage_extractor(source, check, testdir, monkeypatch):  #pylint: disable=W0613
    outdir = testdir.tmpdir
    cmd = f'-i {source} -o {outdir} --title --page=0'

    tests.detector_.run(cmd, monkeypatch=monkeypatch)

    source = detector.path.titlepage(outdir)
    titlepage = serializeraw.load_titlepage(source)
    check(titlepage)
