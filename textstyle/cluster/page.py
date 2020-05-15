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


class ClusterProperty(enum.Enum):
    SIZE = enum.auto()
    FONT = enum.auto()
    BEFORE = enum.auto()
    AFTER = enum.auto()
    YPOS = enum.auto()


ClusterPropertySelection = typing.List[ClusterProperty]


def cluster(
        items: textstyle.TextProperties,
        selection: ClusterPropertySelection = None,
        validator: callable = None,
        *,
        minsize: int = 5,  # TODO: HOLY VALUE
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
    return clustered


def text(flats, returncluster: bool = False):
    clustered = cluster(flats, (ClusterProperty.SIZE, ClusterProperty.FONT))
    result = bestmatch(clustered)
    if returncluster:
        return result, clustered[0]
    return result


def pagenumber(flats, returncluster: bool = False):
    clustered = cluster(
        flats,
        (ClusterProperty.SIZE, ClusterProperty.FONT),
        validator=lambda item: item.length <= 6,
    )
    # assert len(clustered) == 1, len(clustered)
    result = bestmatch(clustered)
    if returncluster:
        return result, clustered[0]
    return result


def bestmatch(clustered, number: int = 0):
    largest_cluster_first_item = clustered[number].content[0]
    size = largest_cluster_first_item.size
    font = largest_cluster_first_item.font
    before = utila.mode([item.before for item in clustered[number].content])
    after = utila.mode([item.after for item in clustered[number].content])
    length = len(clustered[0])
    return (size, font, length, (before, after))


def headlines(
        flats: textstyle.TextProperties,
        min_headline_count: int = 3,
        greater_than_text: bool = True,
):
    _text = text(flats, returncluster=True)
    _pagenumber = pagenumber(flats, returncluster=True)

    flats = remove(flats, _text[1])
    flats = remove(flats, _pagenumber[1])

    textsize = _text[0][0]
    text_before, text_after = _text[0][3]

    if greater_than_text:
        flats = [item for item in flats if item.size >= textsize]

    def valid_headline(item) -> bool:
        if item.before is None:
            return True
        if item.before <= text_before * 1.2:  # TODO: HOLY VALUE
            return False
        if item.after is None:
            return False
        if item.after <= text_after * 1.2:  # TODO: HOLY VALUE
            return False
        return True

    clustered = cluster(
        flats,
        (ClusterProperty.SIZE,),
        validator=valid_headline,
        minsize=min_headline_count,
    )

    largest_font_size = sorted(
        clustered,
        key=lambda x: x.content[0].size,
        reverse=True,
    )

    result = []
    for index in range(5):
        # analyse maximal five headline levels
        try:
            matched = bestmatch(largest_font_size, number=index)  # pylint:disable=C0103
        except IndexError:
            break
        else:
            result.append(matched)
    return result


def remove(flats, toremove: list):
    toremove = set(toremove)
    flats = [item for item in flats if item not in toremove]
    return flats
