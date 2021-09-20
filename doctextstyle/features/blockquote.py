# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import utila

MIN_BLOCKQUOTE_CLUSTER_SIZE = 30

MAX_BLOCKQUOTE_LEFT_DIFF = 15.0
MAX_BLOCKQUOTE_RIGHT_DIFF = 15.0

MIN_BLOCKQUOTE_TEXT_LENGTH = 45


def blockquote_style(flats) -> tuple:
    # TODO: REMOVE TEXT CLUSTER FIRST
    flats = [item for item in flats if item.hashed.count('.') < 10]
    # skip very short text
    flats = [
        item for item in flats if len(item.hashed) > MIN_BLOCKQUOTE_TEXT_LENGTH
    ]
    # skip item which start too right
    flats = [item for item in flats if item.left <= 160]
    # cluster text
    clustered = utila.determine_cluster(
        flats,
        classifier=classifier,
        min_elements=MIN_BLOCKQUOTE_CLUSTER_SIZE,
        strategy=utila.MatchStrategy.MIN,
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
    leftdiff = utila.near(x00, x0, diff=MAX_BLOCKQUOTE_LEFT_DIFF)
    if not leftdiff:
        return None
    rightdiff = utila.near(x11, x1, diff=MAX_BLOCKQUOTE_RIGHT_DIFF)
    if not rightdiff:
        return None
    # use minimal diff classifier
    return math.fabs(x00 - x0) + math.fabs(x11 - x1)
