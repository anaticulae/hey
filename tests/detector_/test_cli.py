# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import tests
import tests.detector_
from tests.resources import HOWTO_PYPORTING
from tests.resources import PYPORTING
from tests.resources import RESTRUCT


@pytest.mark.parametrize('command', [
    ['--help'],
    ['--version'],
])
def test_detector_misc(command, testdir, monkeypatch, capsys):  #pylint: disable=W0613
    """Run help and version command to reach basic test coverage"""
    tests.detector_.run(command, monkeypatch=monkeypatch)

    tests.write_capsys(capsys)


@pytest.mark.parametrize('example', [
    pytest.param(HOWTO_PYPORTING, id='howto_pyporting'),
    pytest.param(RESTRUCT, id='restructured'),
    pytest.param(PYPORTING, id='pyporting'),
])
@utila.skip_longrun
def test_detector_run_work(example, testdir, monkeypatch, capsys):  #pylint: disable=W0613
    output = str(testdir)
    command = f'-i {example} -o {output}'

    with utila.increased_filecount(output, mindiff=2, maxdiff=2):
        tests.detector_.run(command, monkeypatch=monkeypatch)

    tests.write_capsys(capsys)
