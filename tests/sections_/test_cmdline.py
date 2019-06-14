# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import mark
from utila import install_and_run
from utila.test import skip_nonvirtual

from sections import PACKAGE_NAME
from sections import PROCESS_NAME
from sections import ROOT
from tests.groupme_ import FOOTER
from tests.sections_ import run_sections_success


@skip_nonvirtual
def test_sections_setup_py():
    """Install sections and run setions --help to ensure basic functionality"""
    install_and_run(ROOT, PACKAGE_NAME, PROCESS_NAME)


@mark.parametrize('command', [
    ['--help'],
    ['-i', FOOTER, '-o', '.', '--title', '--toc', '--index'],
])
def test_run_sections(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_sections_success(command, monkeypatch=monkeypatch)
