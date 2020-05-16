# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum
import typing

import utila

import hey.classificator
import textstyle
import textstyle.utils


class ClusterProperty(enum.Enum):
    SIZE = enum.auto()
    FONT = enum.auto()
    BEFORE = enum.auto()
    AFTER = enum.auto()
    YPOS = enum.auto()


ClusterPropertySelection = typing.List[ClusterProperty]


def cluster(  # pylint:disable=R1260
        items: textstyle.TextProperties,
        selection: ClusterPropertySelection = None,
        validator: callable = None,
        *,
        minsize: int = 5,  # TODO: HOLY VALUE
        unique_content: bool = False,
):
    if selection:
        selection = set(selection)
    if validator:
        items = [item for item in items if validator(item)]

    def classifier(candidat, clusteritem):
        if selection is None or ClusterProperty.SIZE in selection:
            if candidat.size != clusteritem.size:
                return False
        if selection is None or ClusterProperty.AFTER in selection:
            if candidat.after != clusteritem.after:
                return False
        if selection is None or ClusterProperty.FONT in selection:
            if candidat.font != clusteritem.font:
                return False
        return True

    clustered = hey.classificator.determine_cluster(
        items,
        classifier=classifier,
        min_elements=minsize,
    )
    if unique_content:
        clustered = [item for item in clustered if iscontent_unique(item)]

    return clustered


def iscontent_unique(current) -> bool:
    expected = len(current.content)
    current = {item.hashed for item in current.content}
    return len(current) == expected


def bestmatch(clustered, number: int = 0):
    try:
        largest_cluster_first_item = clustered[number].content[0]
    except IndexError:
        # no clusted content
        return None
    size = largest_cluster_first_item.size
    font = largest_cluster_first_item.font
    # TODO: PLUS INF OR MINUS INF
    before = [item.before for item in clustered[number].content]
    before = [utila.INF if item is None else item for item in before]
    before = utila.mode(before)
    after = [item.after for item in clustered[number].content]
    after = [utila.INF if item is None else item for item in after]
    after = utila.mode(after)
    length = len(clustered[0])

    if before is utila.INF:
        before = None
    if after is utila.INF:
        after = None
    return (size, font, length, (before, after))


def remove(flats, toremove: list):
    toremove = set(toremove)
    flats = [item for item in flats if item not in toremove]
    return flats
