# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import serializeraw
import utilo
import utilo.math

PAGESIZE_DISTANCE_MAX = configos.HV_FLOAT_PLUS(default=5.0)

PAGESIZE_COUNT_MIN = configos.HV_INT_PLUS(default=3)


def pagesizes(path, pages: tuple = None):
    loaded = serializeraw.load_pageborders(path, pages=pages)

    pagesizes_ = [tuple(item.size) for item in loaded]

    def equals(candidat, clusteritem):
        distance = utilo.length(*candidat, *clusteritem)
        return distance < PAGESIZE_DISTANCE_MAX

    clustered = utilo.determine_cluster(
        pagesizes_,
        classifier=equals,
        min_elements=PAGESIZE_COUNT_MIN,
    )

    result = [(item[0], len(item)) for item in clustered]
    return result
