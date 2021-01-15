# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila

import caption.path
import tests.caption_
import tests.caption_.utils
import tests.resources


def test_caption_cli_help(monkeypatch):
    tests.caption_.run('--help', monkeypatch=monkeypatch)


@pytest.mark.parametrize('page, expected', [
    (18, 1),
    (21, 2),
])
def test_caption_bachelor90_pagex(page, expected, testdir, monkeypatch):
    source = power.BACHELOR090_PDF
    extracted = tests.caption_.utils.extract_captions(
        source,
        page,
        testdir,
        monkeypatch,
    )
    content = utila.select_content(extracted, page)
    assert len(content) == expected


def test_caption_bachelor90_page80(testdir, monkeypatch):
    source = power.BACHELOR090_PDF
    extracted = tests.caption_.utils.extract_captions(
        source,
        80,
        testdir,
        monkeypatch,
        caption.path.table_caption,
    )
    tables = extracted[0].content
    assert len(tables) == 1, str(tables)


def test_caption_master116_page12(testdir, monkeypatch):
    source = power.MASTER116_PDF
    extracted = tests.caption_.utils.extract_captions(
        source,
        12,
        testdir,
        monkeypatch,
        caption.path.figure_caption,
    )

    figures = extracted[0].content
    assert len(figures) == 2, str(figures)

    caption_2_1 = figures[0]
    assert caption_2_1.line == 4
    assert caption_2_1.lineend == 5

    caption_2_2 = figures[1]
    assert caption_2_2.line == 14
    assert caption_2_2.lineend == 16
