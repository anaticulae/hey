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

import groupme.footer.pages
import tests.resources


@pytest.mark.parametrize('document, pages, expected_pagenumbers', [
    pytest.param(
        tests.resources.HOWTO_ARGPARSE,
        tests.resources.HOWTO_ARGPARSE_PAGE_COUNT,
        tests.resources.HOWTO_ARGPARSE_PAGE_COUNT,
        id='howtoargparse',
    ),
    pytest.param(
        tests.resources.TECHNICAL_24PAGES,
        tests.resources.TECHNICAL_24PAGES_PAGE_COUNT,
        tests.resources.TECHNICAL_24PAGES_PAGE_COUNT - 1,
        id='technical24pages',
    ),
])
def test_footer_pagenumber_strategy(
        document,
        pages,
        expected_pagenumbers,
):
    pages = tuple(range(pages))
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

    strategy = groupme.footer.pages.PageNumberStrategy(
        horizontallines,
        sizeandborder,
        pagenumbers,
    )
    result = strategy.result()
    assert result is not None, result
    assert len(result) == expected_pagenumbers, result
