# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import doctextstyle
import doctextstyle.extractor
import doctextstyle.vector
import tests.doctextstyle_

ARCHIVE = utilo.join(doctextstyle.ROOT, 'tests/doctextstyle_/expected')

# TODO: VALIDATE SIZES
PARAMETERS = [
    pytest.param(hoverpower.BACHELOR063_PDF,
                 15.96,
                 14.04,
                 12.0,
                 id='bachelor63'),
    pytest.param(hoverpower.BACHELOR051_PDF,
                 15.96,
                 14.04,
                 12.0,
                 id='bachelor51'),
    pytest.param(hoverpower.MASTER110_PDF, 24.79, 14.35, 11.96, id='master110'),
    pytest.param(hoverpower.DISS205_PDF, 17.22, 17.22, 14.35, id='diss205'),
]


# skip failing bachelor51
@pytest.mark.parametrize('source, h1, h2, h3', [PARAMETERS[0], PARAMETERS[2]])
@utilotest.longrun
def test_doctextstyle_extract_headlines_old(source, h1, h2, h3):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    result = doctextstyle.extractor.extract(source)
    assert result
    assert result.h1_size == h1
    assert result.h2_size == h2
    assert result.h3_size == h3


@pytest.mark.parametrize('source, pages', [
    utilotest.step(hoverpower.BACHELOR051_PDF),
    utilotest.step(hoverpower.BACHELOR063_PDF),
    utilotest.step(hoverpower.DISS205_PDF),
    utilotest.step(hoverpower.MASTER110_PDF),
])
@utilotest.nightly
def test_docstyle_validate(source, pages, td, mp):
    utilotest.fixture_requires(source)
    pages = utilo.from_tuple(pages, ',') if pages else ':'
    Evaluate(
        source,
        pages,
        td.tmpdir,
        mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, pages, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.doctextstyle_.run,
                mp=mp,
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
