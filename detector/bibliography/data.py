# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BibliographyReference
=====================

Sorting
-------

We sort by family name and as tybreaker by year. If no name is given, we
use `o. V. = ohne Verfasser` instead. If no year is given, we sort it
after the items with year.

# TODO: ADD OTHER SORTING AS THEISSEN recommends
"""

import texmex.alpha
import utila


def theissen_sort(items):
    """We sort by family name and as tybreaker by year. If no name is
    given, we use `o. V. = ohne Verfasser` instead. If no year is given,
    we sort it after the items with year."""
    # sort by year
    items = sorted(
        items,
        key=lambda x: x.year if x.year is not None else utila.INF,
    )
    # sort by author name
    items = sorted(
        items,
        key=lambda x: texmex.alpha.replace(x.author).lower()
        if x.author else 'o. V.',
    )
    return items
