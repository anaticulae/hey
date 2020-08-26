# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw
import power
import pytest
import serializeraw

import tests.groupme_


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.MASTER116_PDF, None, 0, id='master116'),
    pytest.param(power.BACHELOR063_PDF, None, 0, id='bachelor63'),
])
def test_footer_validate(source, pages, expected, testdir, monkeypatch):
    pages = '' if pages is None else f'--pages={pages}'
    cmd = f'-i {power.link(source)}  --footer {pages}'
    tests.groupme_.run(cmd, monkeypatch=monkeypatch)
    headerpath = iamraw.path.headerfooters(testdir.tmpdir)

    loaded = serializeraw.load_headerfooter(headerpath)
    content = []
    for page in loaded:
        if not page.footer:
            continue
        with contextlib.suppress(AttributeError):
            content.extend(page.footer.notes)
    expected = 0 if expected is None else expected
    assert len(content) == expected, len(content)
