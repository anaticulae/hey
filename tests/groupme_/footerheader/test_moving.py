# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import groupme.feature.footer
import groupme.footer.strategy.moving
import groupme.footer.strategy.plainmoving


def validate_master72(result):
    first_notes = utila.select_page(result, page=3).footer.notes
    assert first_notes[0].number == 1, first_notes[0].number


def validate_bachelor90(result):
    footnotes = flat_footnotes(result)  # pylint:disable=W0612
    numbers = [item.number for item in footnotes]
    assert numbers == list(range(12))


def validate_homework18(result):
    footnotes = flat_footnotes(result)  # pylint:disable=W0612


@pytest.mark.parametrize(
    'document, pages, expected_footer, strategy, validate', [
        pytest.param(
            power.link(power.MASTER072_PDF),
            tuple(range(20)),
            [(3, 6), (6, 3), (7, 2), (8, 4), (9, 1), (10, 4), (11, 3), (12, 2),
             (13, 6), (14, 7), (15, 8), (16, 10), (17, 8), (18, 7), (19, 8)],
            groupme.footer.strategy.moving.MovingFooterStrategy,
            validate_master72,
            id='master72pages',
        ),
        pytest.param(
            power.link(power.BACHELOR111_PDF),
            tuple(range(20)),
            [(9, 2), (10, 3), (11, 2), (12, 1), (13, 1), (15, 2), (16, 1),
             (17, 8), (18, 3), (19, 1)],
            groupme.footer.strategy.moving.MovingFooterStrategy,
            None,
            id='bachelor111pages',
        ),
        pytest.param(
            power.link(power.DOCU27_PDF),
            tuple(range(20)),
            [],
            groupme.footer.strategy.moving.MovingFooterStrategy,
            None,
            id='restructured',
        ),
        pytest.param(
            power.link(power.HOMEWORK018_PDF),
            tuple(range(6)),
            [(3, 3), (4, 4), (5, 7)],
            groupme.footer.strategy.plainmoving.PlainMovingFooterStrategy,
            validate_homework18,
            id='home18',
        ),
        pytest.param(
            power.link(power.BACHELOR090_PDF),
            tuple(range(18, 25)),
            [(18, 2), (19, 1), (21, 1), (22, 3), (23, 4)],
            groupme.footer.strategy.moving.MovingFooterStrategy,
            validate_bachelor90,
            id='bachelor90',
            marks=pytest.mark.xfail(reason='pdf is not printed correctly'),
        ),
    ])
@utilatest.skip_longrun
def test_groupme_footer_moving(
        document,
        pages,
        expected_footer,
        strategy,
        validate,
):
    """Hint: This test is dependend on moving footer strategy. If this
    test fails, may the footer is not extracted correctly. Look at the
    holy value in moving.py:extract_footer."""
    strategy = groupme.footer.strategy.create_strategy(
        path=document,
        strategy=strategy,
        pages=pages,
    )
    result = strategy.result()

    if validate:
        validate(result)

    footer = [item for item in result if item.footer]
    assert len(footer) == len(expected_footer), footer

    for page, length in expected_footer:
        extracted_footer = utila.select_page(result, page)
        notes = extracted_footer.footer.notes
        assert len(notes) == length, f'on page: {page}'
        assert extracted_footer[1], utila.log_raw(f'has no footer: {page}')


def test_groupme_footer_master72pages(testdir):
    path = iamraw.path.horizontals(power.link(power.MASTER072_PDF))
    result = serializeraw.load_horizontals(path)
    assert len(result) > 10, str(result)


def flat_footnotes(pages):
    result = []
    for page in pages:
        result.extend(page.footer)
    return result
