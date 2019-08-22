# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila
from utila import install_and_run
from utila.test import skip_nonvirtual

from detector import PACKAGE_NAME
from detector import PROCESS_NAME
from detector import ROOT
from tests import write_capsys
from tests.detector_ import run_detector_success


@skip_nonvirtual
@utila.skip_longrun
def test_detector_setup_py():
    """Install words and run setions --help to ensure basic functionality"""
    install_and_run(ROOT, PACKAGE_NAME, PROCESS_NAME)


@pytest.mark.parametrize('command', [
    ['--help'],
    ['--version'],
])
def test_detector_run(command, testdir, monkeypatch, capsys):  #pylint: disable=W0613
    """Run help and version command to reach basic test coverage"""
    run_detector_success(command, monkeypatch=monkeypatch)

    write_capsys(capsys)
