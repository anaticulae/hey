# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import tests.groupme_
import tests.resources


@pytest.mark.parametrize('cmd', [
    ['--help'],
    ['-i', tests.resources.HOWTOWRITE9, '-o', 'output'],
    ['-i', tests.resources.MASTER72, '-o', 'output'],
    ['-i', tests.resources.MASTER89, '-o', 'output'],
    ['-i', tests.resources.PYPORTING, '-o', 'output'],
    ['-i', tests.resources.RESTRUCT, '-o', 'output'],
    ['-i', tests.resources.HOWTO_PYPORTING, '-o', 'output'],
])
@pytest.mark.usefixtures('testdir')
@utila.skip_longrun
def test_groupme_run_external(cmd, monkeypatch):
    """Run help and version and format command to reach basic test coverage"""
    tests.groupme_.run_success(cmd, monkeypatch=monkeypatch)


@utila.skip_longrun
def test_regression_groupme_problem(testdir, monkeypatch):
    """There was a problem with not sorted page numbers which leads
    to duplicated header/footer. This was solved by sorting page number
    of left/right page numbers."""
    tests.groupme_.run_success(
        f'-i {tests.resources.BACHELOR56} -j=8',
        monkeypatch=monkeypatch,
    )
