# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw

import hey.geometry.alternate
import tests.resources


@pytest.mark.parametrize('page, expected', [
    (97, 14),
    (98, 14),
    (99, 15),
    (100, 3),
])
def test_parse_alternate_master116_page(page, expected):
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.MASTER116,
        prefix='oneline',
        pages=page,
    )
    parsed = hey.geometry.alternate.parse_page(navigators[0])
    assert len(parsed) == expected, str(parsed)


def test_parse_alternate_master89_external_liningpoints():
    """Page 80 has to few content items to determine the lining points.
    Therefore the external lining points of page 79 are used to
    determine the bibliograpy on page 80.
    """
    pages = (79, 80)
    expected = (14, 1)
    parsed = load_and_parse(pages, tests.resources.MASTER89)
    for page_result, page_expected in zip(parsed, expected):
        assert len(page_result) == page_expected, str(page_result)


def test_parse_alternate_master89_external_liningpoints_single():
    pages = 79
    parsed = load_and_parse(pages, tests.resources.MASTER89)[0]
    assert len(parsed) == 14, str(parsed)


def test_parse_alternate_bachelor56_page49_whitespace_error():
    pages = (49)
    parsed = load_and_parse(pages, tests.resources.BACHELOR56)[0]
    assert len(parsed) == 8, str(parsed)


def load_and_parse(pages, resources: str):
    navigators = serializeraw.create_pagetextnavigators_frompath(
        resources,
        prefix='oneline',
        pages=pages,
    )
    config = hey.geometry.alternate.ParserConfig(
        min_content_length=10,
        min_word_count=4,
    )
    parsed = hey.geometry.alternate.parse_pages(navigators, config=config)
    return parsed
