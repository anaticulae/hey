# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import magic.data
import magic.path
import tests.magic_
import tests.resources


def test_magic(monkeypatch):
    tests.magic_.run('--help', monkeypatch=monkeypatch)


def test_master72_list_and_blockquotes(testdir, monkeypatch):
    tests.magic_.run(
        (f'-i {tests.resources.MASTER72_SECTIONS_AND_WORDS} '
         f'-i {tests.resources.MASTER72} --pages=0:16'),
        monkeypatch=monkeypatch,
    )

    path = magic.path.content(testdir.tmpdir)
    loaded = magic.data.load_types(path)
    assert loaded

    list_page = utila.select_page(loaded, 7).content
    list_page = [item[1] for item in list_page]
    assert magic.data.ContentType.LIST in list_page

    blockquote_page = utila.select_page(loaded, 14).content
    blockquote_page = [item[1] for item in blockquote_page]
    assert magic.data.ContentType.BLOCKQUOTE in blockquote_page
