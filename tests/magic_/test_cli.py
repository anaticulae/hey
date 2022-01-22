# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila

import magic.path
import tests.caption_
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
    loaded = serializeraw.load_types(path)
    assert loaded

    list_page = utila.select_content(loaded, 7)
    list_page = [item[1] for item in list_page]
    assert iamraw.PageContentType.LIST in list_page

    blockquote_page = utila.select_content(loaded, 14)
    blockquote_page = [item[1] for item in blockquote_page]
    assert iamraw.PageContentType.BLOCKQUOTE in blockquote_page


def run_magic(
    source,
    testdir,
    monkeypatch,
    pages: str = '',
) -> iamraw.PageContentContentTypes:
    source = power.link(source)
    tests.magic_.run(
        f'-i {source} --pages={pages} ',
        monkeypatch=monkeypatch,
    )
    path = magic.path.content_oneline(testdir.tmpdir)
    loaded = serializeraw.load_types(path)
    assert loaded, str(loaded)
    return loaded


@pytest.mark.xfail(reason='improve table skipper')
def test_bachelor90_table_page76(testdir, monkeypatch):
    loaded = run_magic(power.BACHELOR090_PDF, testdir, monkeypatch, pages=76)
    loaded = loaded[0].content
    # single caption, table content is removed
    assert len(loaded) == 1


@pytest.mark.xfail(reason='table content skipping changes result')
def test_magic_multiple_line_master116_page79(testdir, monkeypatch):
    """Ensure to handle multiple line captions/magic correctly."""
    source = power.link(power.MASTER116_PDF)
    cmd = f'-i {source}  --pages=79'
    # generate required caption for magic module
    tests.caption_.run(cmd, monkeypatch=monkeypatch)
    tests.magic_.run(cmd, monkeypatch=monkeypatch)

    path = magic.path.content_oneline(testdir.tmpdir)
    loaded = serializeraw.load_types(path)[0].content
    assert loaded

    contenttype = {
        item[0] for item in loaded if item[1] == iamraw.PageContentType.CAPTION
    }
    # TODO: adjust expected after changing table content skipper
    expected = {8, 9, 24, 25}
    assert contenttype == expected
