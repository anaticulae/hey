# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import tests.fixtures
import tests.resources
from tests import write_capsys
from tests.resources import RESTRUCT
from tests.words_ import run_words_success


@pytest.mark.parametrize('command', [
    ['--help'],
    ['--version'],
    ['-i', RESTRUCT, '-o', '.'],
    ['-i', RESTRUCT, '-o', '.', '--pages', '0:9'],
])
def test_words_run(command, testdir, monkeypatch, capsys):  #pylint: disable=W0613
    """Run help and version command to reach basic test coverage"""
    run_words_success(command, monkeypatch=monkeypatch)

    write_capsys(capsys)


def test_words_feature_words_work_pages0_10(testdir, monkeypatch):
    root = str(testdir)
    cmd = f'-i {root} -o {root} --pages=0:10'

    tests.fixtures.setup_testresources(
        source=tests.resources.MASTER_72PAGES,
        dest=root,
        accept=['rawmaker', 'sections', 'groupme'],
    )

    run_words_success(cmd, monkeypatch=monkeypatch)
