# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import doctextstyle
import doctextstyle.extractor
import doctextstyle.vector
import tests.doctextstyle_

ARCHIVE = utila.join(doctextstyle.ROOT, 'tests/doctextstyle_/expected')

# TODO: VALIDATE SIZES
PARAMETERS = [
    pytest.param(power.BACHELOR063_PDF, 15.96, 14.04, 12.0, id='bachelor63'),
    pytest.param(power.BACHELOR051_PDF, 15.96, 14.04, 12.0, id='bachelor51'),
    pytest.param(power.MASTER110_PDF, 24.79, 14.35, 11.96, id='master110'),
    pytest.param(power.DISS205_PDF, 17.22, 17.22, 14.35, id='diss205'),
]


# skip failing bachelor51
@pytest.mark.parametrize('source, h1, h2, h3', [PARAMETERS[0], PARAMETERS[2]])
@utilatest.longrun
def test_doctextstyle_extract_headlines_old(source, h1, h2, h3):
    utilatest.fixture_requires(source)
    source = power.link(source)
    result = doctextstyle.extractor.extract(source)
    assert result
    assert result.h1_size == h1
    assert result.h2_size == h2
    assert result.h3_size == h3


@pytest.mark.parametrize('source, pages', [
    utilatest.step(power.BACHELOR051_PDF),
    utilatest.step(power.BACHELOR063_PDF),
    utilatest.step(power.DISS205_PDF),
    utilatest.step(power.MASTER110_PDF),
])
@utilatest.nightly
def test_docstyle_validate(source, pages, testdir, monkeypatch):
    pages = utila.from_tuple(pages, ',') if pages else ':'
    Evaluate(
        source,
        pages,
        testdir.tmpdir,
        monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.doctextstyle_.run,
                monkeypatch=monkeypatch,
            ),
            step='',
            source=source,
            pages=pages,
            workdir=workdir,
            archive=ARCHIVE,
            loader=serializeraw.load_doctextstyle,
        )

    def raw(self, value) -> str:
        return str(value)
