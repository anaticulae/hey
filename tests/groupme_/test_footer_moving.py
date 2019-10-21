# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw
import utila

import groupme.feature.footer
import groupme.footer.moving
import tests.fixtures.restruct
import tests.resources


@pytest.mark.parametrize('document, pages, expected_footer', [
    pytest.param(
        tests.resources.MASTER_72PAGES,
        tuple(range(20)),
        [(3, 6), (6, 3), (7, 2), (8, 4), (9, 1), (10, 4), (11, 3), (12, 2),
         (13, 6), (14, 7), (15, 8), (16, 10), (17, 8), (18, 7), (19, 8)],
        id='master72pages',
    ),
    pytest.param(
        tests.resources.BACHELOR_111PAGES,
        tuple(range(20)),
        [(9, 2), (10, 3), (11, 2), (12, 1), (13, 1), (15, 2), (16, 1), (17, 8),
         (18, 3), (19, 1)],
        id='bachelor111pages',
    ),
    pytest.param(
        tests.resources.RESTRUCT,
        tuple(range(20)),
        [],
        id='restructured',
    ),
])
def test_groupme_footer_moving(document, pages, expected_footer):
    strategy = groupme.footer.create_strategy(
        path=document,
        strategy=groupme.footer.moving.MovingFooterStrategy,
        pages=pages,
    )
    result = strategy.result()

    footer = [item for item in result if item.footer]
    assert len(footer) == len(expected_footer), footer

    for page, length in expected_footer:
        extracted_footer = utila.select_page(result, page)
        notes = extracted_footer.footer.notes
        assert len(notes) == length
        assert extracted_footer[1], utila.log_raw(f'has no footer: {page}')


def test_groupme_footer_master72pages(testdir):
    path = tests.resources.horizontals(tests.resources.MASTER_72PAGES)
    result = serializeraw.load_horizontals(path)
    assert len(result) > 10, str(result)
