# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import serializeraw
import utila

import detector
import detector.feature.titlepage
import tests


def test_titlepage_parser():
    extracted = detector.feature.titlepage.work(
        tests.resources.SIMPLE_ONELINE_TEXT,
        tests.resources.SIMPLE_ONELINE_POSITION,
    )
    assert extracted

    # ensure that result is converted to yaml
    assert isinstance(extracted, str), type(extracted)


def test_detector_feature_titlepage_complete(testdir, monkeypatch):
    """Intergration test to ensure that rawmaker -> detector works correctly"""
    root = str(testdir)
    cmd = (f'rawmaker -i {tests.resources.MASTER_72PAGES} --pages=0 '
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
