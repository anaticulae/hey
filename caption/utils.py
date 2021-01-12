# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator


def sorted_bounds(items):
    if not items:
        return []
    result = [item.bounding for item in items.content]
    # left to right
    result = sorted(result, key=operator.itemgetter(0))
    # top to down
    result = sorted(result, key=operator.itemgetter(3))
    return result
