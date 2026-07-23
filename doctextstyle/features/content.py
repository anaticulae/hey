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

CONTENT_DIFF_MAX = configos.HV_FLOAT_PLUS(default=5.0)

CONTENT_ELEMENTS_MIN = configos.HV_INT_PLUS(default=3)


def content(path, pages: tuple = None):
    leftright = serializeraw.load_leftright_border(path, pages)

    def equals(candidat, clusteritem):
        # left, right, top, down
        distance = utilo.norms(candidat, clusteritem)
        return distance < CONTENT_DIFF_MAX

    clustered = utilo.determine_cluster(
        leftright.values(),
        classifier=equals,
        min_elements=CONTENT_ELEMENTS_MIN,
    )
    # TODO: SUPPORT LEFT AND RIGHT DIFFERENT PAGE?
    result = [(cluster[0], len(cluster)) for cluster in clustered]
    return result
