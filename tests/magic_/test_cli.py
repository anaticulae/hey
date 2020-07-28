# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import magic.data
import magic.path
import tests.magic_
import tests.resources


def test_magic(monkeypatch):
    tests.magic_.run('--help', monkeypatch=monkeypatch)


def test_master72_list_and_blockquotes(testdir, monkeypatch):
    tests.magic_.run(
        (f'-i {power.link(power.MASTER072_PDF, folder="sectionsandwords")} '
         f'-i {power.link(power.MASTER072_PDF)} --pages=0:16'),
        monkeypatch=monkeypatch,
    )

    path = magic.path.content(testdir.tmpdir)
    loaded = magic.data.load_types(path)
    assert loaded

    list_page = utila.select_content(loaded, 7)
    list_page = [item[1] for item in list_page]
    assert magic.data.ContentType.LIST in list_page

    blockquote_page = utila.select_content(loaded, 14)
    blockquote_page = [item[1] for item in blockquote_page]
    assert magic.data.ContentType.BLOCKQUOTE in blockquote_page


def test_bachelor90_table_page76(testdir, monkeypatch):
    tests.magic_.run(
        f'-i {power.link(power.BACHELOR090_PDF)} --pages=76 ',
        monkeypatch=monkeypatch,
    )
    path = magic.path.content(testdir.tmpdir)
    loaded = magic.data.load_types(path)[0].content
    assert loaded, str(loaded)
    assert len(loaded) == 15  # TODO: NOT VERIFIED
