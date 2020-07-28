# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import utila

MIN_BLOCKQUOTE_CLUSTER_SIZE = 30

MAX_BLOCKQUOTE_LEFT_DIFF = 10.0
MAX_BLOCKQUOTE_RIGHT_DIFF = 10.0

MIN_BLOCKQUOTE_TEXT_LENGTH = 45


def blockquote_style(flats) -> tuple:
    # TODO: REMOVE TEXT CLUSTER FIRST
    flats = [item for item in flats if item.hashed.count('.') < 10]

    flats = [
        item for item in flats if len(item.hashed) > MIN_BLOCKQUOTE_TEXT_LENGTH
    ]

    flats = [item for item in flats if item.left <= 160]

    def classifier(candidat, clusteritem):
        x0 = clusteritem.left
        x1 = clusteritem.right

        x00 = candidat.left
        x11 = candidat.right

        if candidat.size != clusteritem.size:
            return False

        if not (utila.near(x00, x0, diff=MAX_BLOCKQUOTE_LEFT_DIFF) and
                utila.near(x11, x1, diff=MAX_BLOCKQUOTE_RIGHT_DIFF)):
            return None
        # use minimal diff classifier
        return math.fabs(x00 - x0) + math.fabs(x11 - x1)

    clustered = utila.determine_cluster(
        flats,
        classifier=classifier,
        min_elements=MIN_BLOCKQUOTE_CLUSTER_SIZE,
        strategy=utila.MatchStrategy.MIN,
    )

    if len(clustered) < 2:
        return None

    # largest cluster is text cluster
    blockquote = clustered[1].center
    return (blockquote.font, blockquote.size, blockquote.left, blockquote.right)
