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
import detector.parser.person
import detector.titlepage
import tests
import tests.fixtures.simple
import tests.resources as tr


@utila.skip_longrun
def test_titlepage_parser():
    extracted = detector.feature.titlepage.work(
        iamraw.path.text(
            tests.resources.HOWTO_PYPORTING,
            prefix='oneline',
        ),
        iamraw.path.textposition(
            tests.resources.HOWTO_PYPORTING,
            prefix='oneline',
        ),
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


def check_116_pages(titlepage: iamraw.TitlePage):
    # TODO: Activate later if we can explain every element on title page
    # assert titlepage.thesis.typ == iamraw.DocumentType.NONE
    assert titlepage.date == iamraw.TitleDate(
        year=2016,
        month=4,
        day=19,
        location='Berlin',
        valid=True,
        raw='Berlin, 19. April 2016',
    )
    # assert titlepage.title == (
    #     'Modellierung und Simulation eines hybriden Lokomotivantriebs mit '
    #     'elektrischem Stufenlosgetriebe'), titlepage.title
    # TODO: REMOVE LATER
    assert titlepage.title == (
        'Modellierung und Simulation eines  hybriden Lokomotivantriebs mit  '
        'elektrischem Stufenlosgetriebe'), titlepage.title

    # TODO: Activate later
    author = iamraw.Person(
        iamraw.AcademicTitle.STUDENT,
        'Fahrendholz',
        'Helmut Konrad',
        'vorgelegt von:\nHelmut Konrad Fahrendholz',
    )
    assert titlepage.author == author


@pytest.mark.parametrize('source, checker', [
    pytest.param(
        tests.resources.MASTER72_PDF,
        check_72_pages,
        id='master72',
    ),
    pytest.param(
        tests.resources.MASTER78_PDF,
        check_78_pages,
        id='master78',
    ),
    pytest.param(
        tests.resources.MASTER116_PDF,
        check_116_pages,
        id='master116',
    ),
])
@utila.skip_longrun
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

    cmd = f'-i {root} --titlepage'
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


def parse_titlepages(path: str, pages: tuple = None):
    navigators = serializeraw.create_pagetextnavigators_frompath(
        path, pages=pages)
    parsed = detector.feature.titlepage.parse_titlepages(navigators, pages)
    return parsed


@utila.skip_longrun
def test_detector_feature_titlepage_select_best():
    pages = tuple(range(20))
    parsed = parse_titlepages(tr.MASTER72, pages=pages)
    best = detector.titlepage.select_best(parsed)
    assert best == parsed[0], str(best)


@utila.skip_longrun
@pytest.mark.parametrize('source', [
    pytest.param(item, id=os.path.split(item)[1])
    for item in tr.NO_TITLE_GENERATED
])
def test_detector_feature_titlepage_select_best_no_titlepage(source):
    pages = tuple(range(20))
    parsed = parse_titlepages(source, pages=pages)
    best = detector.titlepage.select_best(parsed)
    assert best is None, str(best)


@pytest.mark.parametrize('pages', [
    range(1, 5),
    range(5, 10),
    range(10, 15),
    range(20, 25),
    range(25, 30),
    range(30, 35),
    range(35, 40),
    range(40, 45),
    range(45, 50),
])
@utila.skip_longrun
def test_detector_feature_titlepage_parse_titlepage_negative(pages):
    """Split pages to increase mutli-process-testing."""
    pages = tuple(pages)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tr.MASTER72,
        pages=pages,
    )
    for page in pages:
        selected = utila.select_page(navigators, page=page)
        parsed = detector.feature.titlepage.parse_titlepages(
            navigators=[selected],
            pages=[page],
        )
        selected = detector.titlepage.select_best(parsed)
        assert not selected, str(f'page: {page}\n{selected}')
