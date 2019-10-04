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

from tests import write_capsys
from tests.resources import RESTRUCT
from tests.words_ import run_words_success
from words import PACKAGE
from words import PROCESS
from words import ROOT


@skip_nonvirtual
@utila.skip_longrun
def test_words_setup_py():
    """Install words and run setions --help to ensure basic functionality"""
    install_and_run(ROOT, PACKAGE, PROCESS)


@pytest.mark.parametrize('command', [
    ['--help'],
    ['--version'],
    ['-i', RESTRUCT, '-o', '.'],
])
def test_words_run(command, testdir, monkeypatch, capsys):  #pylint: disable=W0613
    """Run help and version command to reach basic test coverage"""
    run_words_success(command, monkeypatch=monkeypatch)

    write_capsys(capsys)
