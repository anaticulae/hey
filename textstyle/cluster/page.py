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


def text(flats, returncluster: bool = False):
    clustered = cluster(flats, (ClusterProperty.SIZE, ClusterProperty.FONT))
    result = bestmatch(clustered)
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

    clustered = cluster(
        flats,
        (ClusterProperty.SIZE, ClusterProperty.FONT),
        validator=validator,
    )
    # assert len(clustered) == 1, len(clustered)
    result = bestmatch(clustered)
    if returncluster:
        return result, clustered[0] if clustered else []
    return result


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


def headlines(  # pylint:disable=R1260,R0914
        flats: textstyle.TextProperties,
        min_headline_count: int = 5,
        greater_than_text: bool = True,
        returncluster: bool = False,
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
    result_cluster = []
    for index in range(5):
        # analyse maximal five headline levels
        matched = bestmatch(largest_font_size, number=index)  # pylint:disable=C0103
        if not matched:
            continue
        result.append(matched)
        result_cluster.append(largest_font_size[index].content)
    if returncluster:
        return result, result_cluster
    return result


MIN_FOOTNOTES_COUNT = 10  # TODO: HOLY VALUE


def footnotes(flats: textstyle.TextProperties):
    _text = text(flats, returncluster=True)
    _pagenumber = pagenumber(flats, returncluster=True)
    _headlines = headlines(flats, returncluster=True)

    flats = remove(flats, _text[1])
    flats = remove(flats, _pagenumber[1])
    for item in _headlines[1]:
        flats = remove(flats, item)

    def validator(item) -> bool:
        # Shrink footnotes to bottom area
        return item.bottom < 150 and item.length >= 25  # TODO:HOLY VALUE

    clustered = cluster(
        flats,
        (ClusterProperty.SIZE,),
        validator=validator,
        minsize=MIN_FOOTNOTES_COUNT,
        unique_content=True,
    )
    result = bestmatch(clustered)
    return result


def remove(flats, toremove: list):
    toremove = set(toremove)
    flats = [item for item in flats if item not in toremove]
    return flats
