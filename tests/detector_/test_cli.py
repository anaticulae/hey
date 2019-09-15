# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

from detector import PACKAGE
from detector import PROCESS
from detector import ROOT
from tests import write_capsys
from tests.detector_ import run_detector_success
from tests.resources import PYPORTING
from tests.resources import RESTRUCT
from tests.resources import SIMPLE


@utila.skip_longrun
@utila.skip_nonvirtual
def test_detector_setup_py():
    """Install words and run setions --help to ensure basic functionality"""
    utila.install_and_run(ROOT, PACKAGE, PROCESS)


@pytest.mark.parametrize('command', [
    ['--help'],
    ['--version'],
])
def test_detector_misc(command, testdir, monkeypatch, capsys):  #pylint: disable=W0613
    """Run help and version command to reach basic test coverage"""
    run_detector_success(command, monkeypatch=monkeypatch)

    write_capsys(capsys)


@pytest.mark.parametrize('example', [
    SIMPLE,
    RESTRUCT,
    PYPORTING,
])
def test_detector_run_work(example, testdir, monkeypatch, capsys):  #pylint: disable=W0613
    output = str(testdir)
    command = f'-i {example} -o {output}'

    run_detector_success(command, monkeypatch=monkeypatch)

    # ensure that process write a file
    written = list(os.scandir(output))
    assert len(written) == 1, str(written)

    write_capsys(capsys)
