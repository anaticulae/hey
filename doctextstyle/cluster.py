# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import enum
import functools
import typing

import iamraw
import utila


class ClusterProperty(enum.Enum):
    SIZE = enum.auto()
    FONT = enum.auto()
    BEFORE = enum.auto()
    AFTER = enum.auto()
    YPOS = enum.auto()
    LEFT = enum.auto()


ClusterPropertySelection = typing.List[ClusterProperty]
Tol = collections.namedtuple('Tol', 'abs, rel')
NO_TOLERANCE = Tol(0.0, 0.0)


def cluster(
        items: iamraw.TextProperties,
        selection: ClusterPropertySelection = None,
        validator: callable = None,
        *,
        minsize: int = 5,  # TODO: HOLY VALUE
        unique_content: bool = False,
        max_size_diff=Tol(0.5, 0.1),  # TODO: HOLY VALUES
        max_after_diff=Tol(2.0, 0.1),
        max_before_diff=Tol(2.0, 0.1),
        max_xleft_diff=Tol(5.0, 0.1),
):
    if selection:
        selection = set(selection)
    if validator:
        items = [item for item in items if validator(item)]

    decider = functools.partial(
        classifier,
        selection=selection,
        max_size_diff=max_size_diff,
        max_after_diff=max_after_diff,
        max_before_diff=max_before_diff,
        max_xleft_diff=max_xleft_diff,
    )
    clustered = utila.determine_cluster(
        todo=items,
        classifier=decider,
        min_elements=minsize,
    )
    if unique_content:
        clustered = [item for item in clustered if iscontent_unique(item)]
    return clustered


def classifier(  # pylint:disable=R1260
        candidat,
        clusteritem,
        selection,
        max_size_diff=Tol(0.5, 0.1),  # TODO: HOLY VALUES
        max_after_diff=Tol(2.0, 0.1),
        max_before_diff=Tol(2.0, 0.1),
        max_xleft_diff=Tol(5.0, 0.1),
) -> bool:
    if selection is None or ClusterProperty.SIZE in selection:
        if not utila.pnear(
                candidat.size,
                clusteritem.size,
                abs_tol=max_size_diff.abs,
                rel_tol=max_size_diff.rel,
        ):
            return False
    if selection is None or ClusterProperty.BEFORE in selection:
        if not utila.pnear(
                candidat.before,
                clusteritem.before,
                abs_tol=max_before_diff.abs,
                rel_tol=max_before_diff.rel,
        ):
            return False
    if selection is None or ClusterProperty.AFTER in selection:
        if not utila.pnear(
                candidat.after,
                clusteritem.after,
                abs_tol=max_after_diff.abs,
                rel_tol=max_after_diff.rel,
        ):
            return False
    if selection is None or ClusterProperty.LEFT in selection:
        if not utila.pnear(
                candidat.left,
                clusteritem.left,
                abs_tol=max_xleft_diff.abs,
                rel_tol=max_xleft_diff.rel,
        ):
            return False
    if selection is None or ClusterProperty.FONT in selection:
        if candidat.font != clusteritem.font:
            return False
    return True


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
