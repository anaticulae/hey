# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import caption
import tests.caption_.utils

TABLE = os.path.join(caption.ROOT, 'tests/caption_/tables')
file_read_table = lambda x: utila.file_read(os.path.join(TABLE, x)).strip()  # pylint:disable=C0103
IMAGE = os.path.join(caption.ROOT, 'tests/caption_/image')
file_read_image = lambda x: utila.file_read(os.path.join(IMAGE, x)).strip()  # pylint:disable=C0103

ARCHIVE = os.path.join(caption.ROOT, 'tests/caption_/expected')
utila.exists_assert(ARCHIVE)


@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR056_PDF, id='bachelor56'),
])
def test_validate_caption_table(source, testdir, monkeypatch):
    """In the current state, the table is not parsed correctly.

    Table one is parsed too small. After improving the table parser,
    labels will be parsed better.
    TODO: UPDATE OUTDATED DOCS?
    """
    expected = file_read_table(utila.file_name(source))
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


BACHELOR51PAGE31 = """\
Tabelle 2: Korrelation nach Pearson (Kreuzung)
Tabelle 3: Ergebnisse der Regressionsanalyse Geschwindigkeit und Bremsreaktionszeit mit der abhängigen Variable Unfall Kreuzung.\
"""


def test_validate_caption_bachelor56page31(testdir, monkeypatch):
    extracted = tests.caption_.utils.extract_captions(
        power.BACHELOR056_PDF,
        '31',
        testdir,
        monkeypatch,
        resultpath=iamraw.path.table_caption,
        selected='--table',
    )
    extracted = utila.flatten(page.content for page in extracted)
    extracted = [utila.normalize_text(caption.raw) for caption in extracted]
    extracted: str = utila.NEWLINE.join(extracted)
    assert extracted == BACHELOR51PAGE31


@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR056_PDF, id='bachelor56'),
])
def test_validate_caption_image(source, testdir, monkeypatch):
    expected = file_read_image(utila.file_name(source))
    extracted = tests.caption_.utils.extract_captions(
        source,
        ':',
        testdir,
        monkeypatch,
        resultpath=iamraw.path.image_caption,
        selected='--image',
    )
    extracted = utila.flatten(page.content for page in extracted)
    extracted = [utila.normalize_text(caption.raw) for caption in extracted]
    extracted: str = utila.NEWLINE.join(extracted)
    utila.log(extracted)
    assert extracted == expected


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR056_PDF, 'bachelor056', id='bachelor056'),
])
def test_caption_validate(source, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=':',
        expected=expected,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.caption_.run,
                monkeypatch=monkeypatch,
            ),
            step=None,
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.headlines = power.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        path = iamraw.path.caption_result(path)
        return serializeraw.load_captions(path)

    def raw(self, value) -> str:
        value = utila.flatten_content(value)
        collected = [utila.normalize_text(item.raw) for item in value]
        collected = sorted(collected, key=utila.alphabetically)
        result = utila.NEWLINE.join(collected)
        return result
