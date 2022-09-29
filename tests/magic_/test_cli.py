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
import utilatest

import magic.path
import tests.magic_
import tests.resources


def run_magic(
    source,
    td,
    mp,
    pages: str = '',
) -> iamraw.PageContentContentTypes:
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.magic_.run(
        f'-i {source} --pages={pages} ',
        mp=mp,
    )
    path = magic.path.content_oneline(td.tmpdir)
    loaded = serializeraw.load_types(path)
    assert loaded, str(loaded)
    return loaded


def test_magic(mp):
    tests.magic_.run('--help', mp=mp)


def test_master72_list_and_blockquotes(td, mp):
    utilatest.fixture_requires(power.MASTER072_PDF, folder='sectionsandwords')
    tests.magic_.run(
        (f'-i {power.link(power.MASTER072_PDF, folder="sectionsandwords")} '
         f'-i {power.link(power.MASTER072_PDF)} --pages=0:16'),
        mp=mp,
    )
    path = magic.path.content(td.tmpdir)
    loaded = serializeraw.load_types(path)
    assert loaded
    list_page = utila.select_content(loaded, 7)
    list_page = [item[1] for item in list_page]
    assert iamraw.PageContentType.LIST in list_page
    blockquote_page = utila.select_content(loaded, 14)
    blockquote_page = [item[1] for item in blockquote_page]
    assert iamraw.PageContentType.BLOCKQUOTE in blockquote_page


@pytest.mark.xfail(reason='???')
def test_bachelor90p76_table(td, mp):
    loaded = run_magic(power.BACHELOR090_PDF, td, mp, pages=76)
    loaded = loaded[0].content
    # single caption, table content is removed
    assert len(loaded) == 1


@pytest.mark.xfail(reason='???')
def test_multiple_line_master116p79():
    """Ensure to handle multiple line captions/magic correctly."""
    source = power.link(power.MASTER116_PDF)
    # load oneline result
    path = magic.path.content_oneline(source)
    loaded = serializeraw.load_magic_types(
        path,
        pages=(79,),
    )[0].content
    assert loaded
    contenttype = {
        item[0] for item in loaded if item[1] == iamraw.PageContentType.CAPTION
    }
    # table content, header and footer are rawmaker_cleaned from code
    expected = {0, 1, 8, 9}
    assert contenttype == expected
