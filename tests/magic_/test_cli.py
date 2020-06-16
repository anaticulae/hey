# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests.magic_
import tests.resources


def test_magic(monkeypatch):
    tests.magic_.run('--help', monkeypatch=monkeypatch)


def test_master72_list(testdir, monkeypatch):
    tests.magic_.run(
        (f'-i {tests.resources.MASTER72_SECTIONS_AND_WORDS} '
         f'-i {tests.resources.MASTER72} --pages=0:10'),
        monkeypatch=monkeypatch,
    )
