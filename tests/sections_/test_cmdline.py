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

from tests.resources import MASTER_72PAGES
from tests.resources import PYPORTING
from tests.resources import RESTRUCT
from tests.resources import RESTRUCT_PDF
from tests.resources import SIMPLE
from tests.sections_ import run_sections_failure
from tests.sections_ import run_sections_success


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


def test_run_sections_multicore(testdir, monkeypatch):
    """Regression test to ensure the correct order of the different
    steps in multicore behavior.

    There was a bug in the order of steps. `sections` step was runned to
    early and the required test data were not generated.

    Solved by: upgrading utila lib.
    """
    root = str(testdir)
    # this step is required, cause the test generator already generates
    # this required items.
    # Copy yaml files which starts with rawmaker or groupme.
    pattern = '[rawmaker|groupme]*.yaml'
    utila.copy_content(MASTER_72PAGES, root, pattern=pattern)

    jobs = 5
    cmd = (f'-j{jobs} -i {root} -o {root} --pages=0:5'
           ' --chapter --index --sections --title --toc --whitepage')
    run_sections_success(cmd, monkeypatch=monkeypatch)
