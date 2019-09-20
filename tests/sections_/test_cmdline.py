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

from sections import PACKAGE
from sections import PROCESS
from sections import ROOT
from tests.resources import MASTER_72PAGES
from tests.resources import PYPORTING
from tests.resources import RESTRUCT
from tests.resources import RESTRUCT_PDF
from tests.resources import SIMPLE
from tests.sections_ import run_sections_failure
from tests.sections_ import run_sections_success


@skip_nonvirtual
@utila.skip_longrun
@pytest.hookimpl(tryfirst=True)
def test_sections_setup_py():
    """Install sections and run setions --help to ensure basic functionality"""
    install_and_run(ROOT, PACKAGE, PROCESS)


@pytest.mark.parametrize('command', [
    ['--help'],
    ['-i', RESTRUCT, '-o', '.', '--all'],
    ['-i', SIMPLE, '-o', '.', '--all'],
    ['-i', PYPORTING, '-o', '.', '--all'],
])
def test_run_sections(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_sections_success(command, monkeypatch=monkeypatch)


@pytest.mark.parametrize('command', [
    ['-i', RESTRUCT_PDF, '-o', '.', '--all'],
])
def test_run_sections_failed(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run `sections` with bad input"""
    run_sections_failure(command, monkeypatch=monkeypatch)


@pytest.mark.xfail(reson='problem in resource order - todo: fix resource order')
def test_run_sections_multicore(testdir, monkeypatch):
    # TODO: THERE IS A PROBLEM WITH MULTIPROCESSING
    root = str(testdir)
    jobs = 2
    cmd = (f'-j{jobs} -i {MASTER_72PAGES} -o {root}'
           ' --chapter --index --sections --title --toc --whitepage')
    run_sections_success(cmd, monkeypatch=monkeypatch)
