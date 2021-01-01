# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import doctextstyle.cluster


def text(flats, returncluster: bool = False):
    clustered = doctextstyle.cluster.cluster(flats, (
        doctextstyle.cluster.ClusterProperty.SIZE,
        doctextstyle.cluster.ClusterProperty.FONT,
    ))
    result = doctextstyle.cluster.bestmatch(clustered)
    if returncluster:
        return result, clustered[0] if clustered else []
    return result


def pagenumber(flats, returncluster: bool = False):

    def validator(item) -> bool:
        if item.top >= 100 and item.bottom >= 100:
            # page number is not in the middle of the page. The page
            # number is located at the top or bottom of the page.
            return False
        return item.length <= 6

    clustered = doctextstyle.cluster.cluster(
        flats,
        (
            doctextstyle.cluster.ClusterProperty.SIZE,
            doctextstyle.cluster.ClusterProperty.FONT,
        ),
        validator=validator,
    )
    # assert len(clustered) == 1, len(clustered)
    result = doctextstyle.cluster.bestmatch(clustered)
    if returncluster:
        return result, clustered[0] if clustered else []
    return result
