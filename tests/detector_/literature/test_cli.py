# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import detector.literature.data
import detector.path
import tests.detector_
import tests.resources


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(tests.resources.BACHELOR63, '59', 12, id='bachelor63'),
    pytest.param(tests.resources.MASTER116, '97,98,99,100', 46, id='master116'),
])
def test_detector_literature_run(source, pages, expected, testdir, monkeypatch):  #pylint: disable=W0613
    root = testdir.tmpdir
    command = f'-i {source} -o {root} --literature --pages={pages}'
    tests.detector_.run_detector_success(command, monkeypatch=monkeypatch)

    outpath = detector.path.literature_detected(root)
    loaded = detector.literature.data.load_literature_reference(outpath)
    assert len(loaded) == expected, str(loaded)
