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

import groupme
import tests.groupme_
import tests.resources


@utila.skip_nonvirtual
@pytest.hookimpl(tryfirst=True)
def test_groupme_install_and_run():
    """Install groupme and run groupme --help to ensure basic function"""
    utila.install_and_run(
        groupme.ROOT,
        groupme.PACKAGE,
        groupme.PROCESS,
    )


# TODO: Implement a new concept
TODO_ERROR = ('concept of splitting with first headline does not work, when '
              'first headline differ from table of content')


@pytest.mark.parametrize('cmd', [
    ['--help'],
    ['-i', tests.resources.SIMPLE, '-o', 'output'],
    ['-i', tests.resources.RESTRUCT, '-o', 'output'],
])
@pytest.mark.usefixtures('testdir')
def test_groupme_run_external(cmd, monkeypatch):
    """Run help and version and format command to reach basic test coverage"""
    tests.groupme_.run_success(cmd, monkeypatch=monkeypatch)
