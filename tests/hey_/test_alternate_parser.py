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
def test_parse_alternate_master116_page_x(page, expected):
    navigators = serializeraw.create_pagetextnavigators_frompath(
        tests.resources.MASTER116,
        pages=page,
        prefix='oneline',
    )
    parsed = hey.geometry.alternate.parse_page(navigators[0])
    assert len(parsed) == expected, str(parsed)
