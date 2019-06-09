# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import mark
from pytest import param
from utila import SUCCESS
from utila.test import run
from utila.test import skip_not_virtual

from groupme import ROOT
from tests.groupme_ import FOOTER
from tests.groupme_ import SIMPLE
from tests.groupme_ import run_success


@skip_not_virtual
def test_run_groupme():
    """Install groupme and run groupme --help to ensure basic function"""
    uninstall = 'pip uninstall hey -y'
    install = 'python setup.py install && groupme --help'

    clean_and_run = uninstall + ' && ' + install
    completed = run(clean_and_run, cwd=ROOT)
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr


# TODO: Implement a new concept
TODO_ERROR = ('concept of splitting with first headline does not work, when '
              'first headline differ from table of content')


@mark.parametrize('command', [
    ['--help'],
    ['-i', SIMPLE, '-o', 'output'],
    param(['-i', FOOTER, '-o', 'output'], marks=mark.xfail(reason=TODO_ERROR)),
])
def test_run_rawmaker(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_success(command, monkeypatch=monkeypatch)
