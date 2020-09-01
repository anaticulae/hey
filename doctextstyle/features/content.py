# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import hey.utils


def content(path, pages: tuple = None):
    leftright = serializeraw.load_leftright_border(path, pages)

    def equals(candidat, clusteritem):
        # left, right, top, down
        distance = hey.utils.lengths(candidat, clusteritem)
        return distance < 5.0  # TODO: HOLY VALUE

    clustered = utila.determine_cluster(
        leftright.values(),
        classifier=equals,
        min_elements=3,  # TODO: HOLY VALUE
    )
    # TODO: SUPPORT LEFT AND RIGHT DIFFERENT PAGE?
    result = [(cluster[0], len(cluster)) for cluster in clustered]
    return result
