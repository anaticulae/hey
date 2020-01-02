# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import pytest
import serializeraw
import utila

import detector.cli
import detector.feature.titlepage
import detector.parser.complete
import detector.titlepage
import hey.textnavigator.navigator as htn
import tests
import tests.resources as tr


def test_titlepage_parser():
    extracted = detector.feature.titlepage.work(
        tests.resources.SIMPLE_ONELINE_TEXT,
        tests.resources.SIMPLE_ONELINE_POSITION,
    )
    assert extracted

    # ensure that result is converted to yaml
    assert isinstance(extracted, str), type(extracted)


def check_72_pages(titlepage: iamraw.TitlePage):
    deparment = titlepage.institution.department
    # TODO: Decide what is the better approach
    # assert deparment == 'Fakultät I – Geisteswissenschaften', str(deparment)
    assert deparment == 'Geisteswissenschaften', str(deparment)


def check_78_pages(titlepage: iamraw.TitlePage):
    assert titlepage.thesis.typ == iamraw.DocumentType.MASTER

    university = titlepage.institution.university
    assert university == 'Technische Universit¨at Darmstadt', str(university)


@pytest.mark.parametrize('source, checker', [
    (tests.resources.MASTER_72PAGES_PDF, check_72_pages),
    (tests.resources.MASTER_78PAGES_PDF, check_78_pages),
])
def test_detector_feature_titlepage_complete(
        source,
        checker,
        testdir,
        monkeypatch,
):
    """Intergration test to ensure that rawmaker -> detector works correctly"""
    root = str(testdir)
    cmd = (f'rawmaker -i {source} --pages=0 '
           f'{detector.feature.titlepage.RAWMAKER_CONFIGURATION}')
    rawmaker__ = utila.run(cmd)
    assert rawmaker__.returncode == utila.SUCCESS, str(rawmaker__)

    cmd = f'-i {root}'
    utila.run_command(
        cmd,
        process=detector.cli.PROCESS,
        main=detector.cli.main,
        success=True,
        monkeypatch=monkeypatch,
    )
    cli = detector.cli
    resultfile = f'{cli.PROCESS}__{cli.TITLEPAGE_STEP}_{cli.TITLEPAGE_OUTPUT}.yaml'
    resultpath = os.path.join(root, resultfile)

    titlepage: iamraw.TitlePage = serializeraw.load_titlepage(resultpath)
    assert titlepage

    checker(titlepage)


def parse_titlepages(path: str):
    navigators = htn.create_pagetextnavigators_frompath(path)
    parsed = detector.feature.titlepage.parse_titlepages(navigators)
    return parsed


def test_detector_feature_titlepage_select_best():
    parsed = parse_titlepages(tr.MASTER_72PAGES)
    best = detector.titlepage.select_best(parsed)
    assert best == parsed[0], str(best)


@pytest.mark.parametrize('source', [
    pytest.param(item, id=os.path.split(item)[1])
    for item in tr.NO_TITLE_GENERATED
])
def test_detector_feature_titlepage_select_best_no_titlepage(source):
    parsed = parse_titlepages(source)
    best = detector.titlepage.select_best(parsed)
    assert best is None, str(best)


def test_detector_feature_titlepage_parse_titlepage_negative():
    navigators = htn.create_pagetextnavigators_frompath(tr.MASTER_72PAGES)
    max_pages = 50  # TODO: extend after improving parser
    for index, navigator in enumerate(navigators[1:max_pages], start=1):
        parsed = detector.feature.titlepage.parse_titlepages(
            navigators=[navigator],
            selected=[index],
        )
        selected = detector.titlepage.select_best(parsed)
        assert not selected, str(f'page: {index}\n{selected}')
