# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw.path
import power
import pytest
import utila

import caption
import tests.caption_.utils

EXPECTED = os.path.join(caption.ROOT, 'tests/caption_/tables')
file_read = lambda x: utila.file_read(os.path.join(EXPECTED, x)).strip()  # pylint:disable=C0103


# yapf:disable
@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR056_PDF, id='bachelor56', marks=pytest.mark.xfail(reason='imporve table parser')),
])
# yapf:enable
def test_validate_caption_table(source, testdir, monkeypatch):
    """In the current state, the table is not parsed correctly.

    Table one is parsed too small. After improving the table parser,
    labels will be parsed better.
    """
    expected = file_read(utila.file_name(source))
    extracted = tests.caption_.utils.extract_captions(
        source,
        ':',
        testdir,
        monkeypatch,
        resultpath=iamraw.path.table_caption,
        selected='--table',
    )
    extracted = utila.flatten(page.content for page in extracted)
    extracted = [utila.normalize_text(caption.raw) for caption in extracted]
    extracted: str = utila.NEWLINE.join(extracted)
    assert extracted == expected
