# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import tests.groupme_


@pytest.mark.parametrize('cmd', [
    ['--help'],
    ['-i', power.link(power.ORDER009_PDF), '-o', 'output'],
    ['-i', power.link(power.MASTER072_PDF), '-o', 'output'],
    ['-i', power.link(power.MASTER089_PDF), '-o', 'output'],
    ['-i', power.link(power.DOCU09_PDF), '-o', 'output'],
    ['-i', power.link(power.DOCU27_PDF), '-o', 'output'],
    ['-i', power.link(power.DOCU07_PDF), '-o', 'output'],
])
@pytest.mark.usefixtures('testdir')
@utilatest.skip_nightly
def test_groupme_run_external(cmd, monkeypatch):
    """Run help and version and format command to reach basic test coverage"""
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)


@utilatest.skip_nightly
def test_regression_groupme_problem(testdir, monkeypatch):
    """There was a problem with not sorted page numbers which leads
    to duplicated header/footer. This was solved by sorting page number
    of left/right page numbers."""
    tests.groupme_.run(
        f'-i {power.link(power.BACHELOR056_PDF)} -j=8',
        monkeypatch=monkeypatch,
    )
