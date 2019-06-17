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
from utila import install_and_run
from utila.test import skip_nonvirtual

from groupme import PROCESS_NAME
from groupme import ROOT
from hey import PACKAGE_NAME
from tests.groupme_ import run_success
from tests.resources import FOOTER
from tests.resources import SIMPLE


@skip_nonvirtual
def test_run_groupme():
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
    param(['-i', FOOTER, '-o', 'output'], marks=mark.xfail(reason=TODO_ERROR)),
])
def test_run_rawmaker(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_success(command, monkeypatch=monkeypatch)
