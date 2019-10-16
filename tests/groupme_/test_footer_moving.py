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
import groupme.footer
import groupme.footer.moving
import tests.fixtures.restruct
import tests.resources


@pytest.mark.parametrize('document, pages, expected_footer', [
    (tests.resources.MASTER_72PAGES, tuple(range(20)),
     [3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]),
])
def test_groupme_footer_moving(document, pages, expected_footer):
    horizontallines = serializeraw.load_horizontals(
        tests.resources.horizontals(document),
        pages,
    )
    sizeandborder = serializeraw.load_pageborders(
        tests.resources.sizeandborder(document),
        pages,
    )

    pagenumbers = serializeraw.load_pagenumbers(
        tests.resources.pagenumbers(document),
        pages,
    )

    pagetextnavigators = tests.fixtures.create_pagetextnavigators(
        document,
        pages,
    )

    strategy = groupme.footer.moving.MovingFooterStrategy(
        horizontallines,
        sizeandborder,
        pagenumbers,
        pagetextnavigators,
    )
    result = strategy.result()

    footer = [item for item in result.values() if item.footer]
    assert len(footer) == len(expected_footer), footer

    for footer in expected_footer:
        extracted_footer = utila.select_page(result, footer)
        assert extracted_footer[1], f'{footer}'


def test_groupme_footer_master72pages(testdir):
    path = tests.resources.horizontals(tests.resources.MASTER_72PAGES)
    result = serializeraw.load_horizontals(path)

    assert len(result) > 10, str(result)
