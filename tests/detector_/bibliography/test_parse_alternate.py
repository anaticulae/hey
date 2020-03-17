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

import detector.bibliography.column
import tests.resources


@pytest.mark.parametrize('pages, expected', [
    (97, 14),
    (98, 14),
    (99, 15),
    (100, 3),
])
def test_parse_bibliography_master116_page_x(pages, expected):
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.MASTER116,
        prefix='oneline',
        pages=pages,
    )
    parsed = detector.bibliography.alternate.extracts(navigators)
    assert len(parsed) == expected, str(parsed)
