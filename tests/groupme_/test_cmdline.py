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

from groupme import PACKAGE_NAME
from groupme import PROCESS_NAME
from groupme import ROOT
from tests.groupme_ import run_success
from tests.resources import RESTRUCT
from tests.resources import SIMPLE


@skip_nonvirtual
def test_install_and_run_groupme():
    """Install groupme and run groupme --help to ensure basic function"""
    install_and_run(
        ROOT,
        PACKAGE_NAME,
        PROCESS_NAME,
    )


# TODO: Implement a new concept
TODO_ERROR = ('concept of splitting with first headline does not work, when '
              'first headline differ from table of content')


@mark.parametrize('command', [
    ['--help'],
    ['-i', SIMPLE, '-o', 'output'],
    ['-i', RESTRUCT, '-o', 'output'],
])
def test_run_groupme(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_success(command, monkeypatch=monkeypatch)
