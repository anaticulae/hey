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

from tests.words_ import run_words_success
from words import PACKAGE_NAME
from words import PROCESS_NAME
from words import ROOT


@skip_nonvirtual
def test_words_setup_py():
    """Install words and run setions --help to ensure basic functionality"""
    install_and_run(ROOT, PACKAGE_NAME, PROCESS_NAME)


@mark.parametrize(
    # TODO: add master --todo to activate more than one feature, see --sections
    'command',
    [
        ['--help'],
    ])
def test_run_sections(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_words_success(command, monkeypatch=monkeypatch)
