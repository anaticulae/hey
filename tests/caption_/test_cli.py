# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila

import caption.path
import caption.serialize
import tests.caption_
import tests.resources


def test_caption_cli_help(monkeypatch):
    tests.caption_.run('--help', monkeypatch=monkeypatch)


@pytest.mark.parametrize('page, expected', [
    (18, 1),
    (21, 2),
])
def test_caption_bachelor90_pagex(page, expected, testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    cmd = f'-i {source} --pages={page}'
    tests.caption_.run(cmd, monkeypatch=monkeypatch)

    path = caption.path.image_caption(testdir.tmpdir)
    loaded = caption.serialize.load_captions(path)
    assert loaded
    content = utila.select_content(loaded, page)
    assert len(content) == expected


def test_caption_bachelor90_page80(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    cmd = f'-i {source} --pages=80'
    tests.caption_.run(cmd, monkeypatch=monkeypatch)

    path = caption.path.table_caption(testdir.tmpdir)
    loaded = caption.serialize.load_captions(path)
    assert loaded

    tables = loaded[0].content
    assert len(tables) == 1, str(tables)


def test_caption_master116_page12(testdir, monkeypatch):
    source = power.link(power.MASTER116_PDF)
    cmd = f'-i {source} --figure --general --pages=12'
    tests.caption_.run(cmd, monkeypatch=monkeypatch)

    path = caption.path.figure_caption(testdir.tmpdir)
    loaded = caption.serialize.load_captions(path)
    assert loaded

    figures = loaded[0].content
    assert len(figures) == 2, str(figures)

    caption_2_1 = figures[0]
    assert caption_2_1.line == 4
    assert caption_2_1.lineend == 5

    caption_2_2 = figures[1]
    assert caption_2_2.line == 14
    assert caption_2_2.lineend == 16
