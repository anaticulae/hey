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

ARCHIVE = os.path.join(caption.ROOT, 'tests/caption_/expected')
utila.exists_assert(ARCHIVE)

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


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR051_PDF, 'bachelor051', id='bachelor051'),
    pytest.param(power.BACHELOR056_PDF, 'bachelor056', id='bachelor056'),
    pytest.param(power.BACHELOR063_PDF, 'bachelor063', id='bachelor063'),
    pytest.param(power.BACHELOR090_PDF, 'bachelor090', id='bachelor090'),
    pytest.param(power.BACHELOR111_PDF, 'bachelor111', id='bachelor111'),
    pytest.param(power.DISS205_PDF, 'diss205', id='diss205'),
    pytest.param(power.MASTER072_PDF, 'master072', id='master072'),
    pytest.param(power.MASTER098_PDF, 'master098', id='master098'),
    pytest.param(power.MASTER099_PDF, 'master099', id='master099'),
    pytest.param(power.MASTER116_PDF, 'master116', id='master116'),
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
