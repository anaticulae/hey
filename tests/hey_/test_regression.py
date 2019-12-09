# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import tests.resources
import tests.sections_


def test_regression_sections_and_words(testdir, monkeypatch):
    """Start with whitepage that leads to some trouble with empty
    navigators and problems in serializeraw module."""
    root = str(testdir)

    pattern = '[rawmaker|groupme]*.yaml'
    utila.copy_content(tests.resources.TWINE_NO_TILE, root, pattern=pattern)

    jobs = 5
    cmd = f'-j{jobs} --all'
    tests.sections_.run_sections_success(cmd, monkeypatch=monkeypatch)

    tests.words_.run_words_success('--all', monkeypatch=monkeypatch)
