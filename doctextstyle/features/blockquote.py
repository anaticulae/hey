# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import utilo

BLOCKQUOTE_CLUSTER_SIZE_MIN = configos.HV_INT_PLUS(default=30)

BLOCKQUOTE_LEFT_DIFF_MAX = configos.HV_FLOAT_PLUS(default=15.0)

BLOCKQUOTE_RIGHT_DIFF_MAX = configos.HV_FLOAT_PLUS(default=15.0)

BLOCKQUOTE_TEXT_LENGTH_MIN = configos.HV_INT_PLUS(default=45)


def blockquote_style(flats) -> tuple:
    # TODO: REMOVE TEXT CLUSTER FIRST
    flats = [item for item in flats if item.hashed.count('.') < 10]
    # skip very short text
    flats = [
        item for item in flats if len(item.hashed) > BLOCKQUOTE_TEXT_LENGTH_MIN
    ]
    # skip item which start too right
    flats = [item for item in flats if item.left <= 160]
    # cluster text
    clustered = utilo.determine_cluster(
        flats,
        classifier=classifier,
        min_elements=BLOCKQUOTE_CLUSTER_SIZE_MIN,
        strategy=utilo.MatchStrategy.MIN,
    )
    if len(clustered) < 2:
        # too few cluster
        return None
    # largest cluster is text cluster
    blockquote = clustered[1].center
    result = (
        blockquote.font,
        blockquote.size,
        blockquote.left,
        blockquote.right,
    )
    return result


def classifier(candidat, clusteritem):
    # expected
    x0 = clusteritem.left
    x1 = clusteritem.right
    # current
    x00 = candidat.left
    x11 = candidat.right
    # compare font size
    if candidat.size != clusteritem.size:
        return False
    leftdiff = utilo.near(x00, x0, diff=BLOCKQUOTE_LEFT_DIFF_MAX)
    if not leftdiff:
        return False
    rightdiff = utilo.near(x11, x1, diff=BLOCKQUOTE_RIGHT_DIFF_MAX)
    if not rightdiff:
        return False
    # merge candidat into cluster
    return True
