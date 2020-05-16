# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import doctextstyle.cluster
import hey.classificator


def text(flats, returncluster: bool = False):
    clustered = doctextstyle.cluster.cluster(flats, (
        doctextstyle.cluster.ClusterProperty.SIZE,
        doctextstyle.cluster.ClusterProperty.FONT,
    ))
    result = doctextstyle.cluster.bestmatch(clustered)
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

    clustered = doctextstyle.cluster.cluster(
        flats,
        (
            doctextstyle.cluster.ClusterProperty.SIZE,
            doctextstyle.cluster.ClusterProperty.FONT,
        ),
        validator=validator,
    )
    # assert len(clustered) == 1, len(clustered)
    result = doctextstyle.cluster.bestmatch(clustered)
    if returncluster:
        return result, clustered[0] if clustered else []
    return result


def headlines(  # pylint:disable=R1260,R0914
        flats: doctextstyle.data.TextProperties,
        min_headline_count: int = 5,
        greater_than_text: bool = True,
        returncluster: bool = False,
):
    _text = text(flats, returncluster=True)
    _pagenumber = pagenumber(flats, returncluster=True)

    flats = doctextstyle.cluster.remove(flats, _text[1])
    flats = doctextstyle.cluster.remove(flats, _pagenumber[1])

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

    clustered = doctextstyle.cluster.cluster(
        flats,
        (doctextstyle.cluster.ClusterProperty.SIZE,),
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
        matched = doctextstyle.cluster.bestmatch(
            largest_font_size,
            number=index,
        )  # pylint:disable=C0103
        if not matched:
            continue
        result.append(matched)
        result_cluster.append(largest_font_size[index].content)
    if returncluster:
        return result, result_cluster
    return result


MIN_FOOTNOTES_COUNT = 10  # TODO: HOLY VALUE


def footnote(flats: doctextstyle.data.TextProperties):
    _text = text(flats, returncluster=True)
    _pagenumber = pagenumber(flats, returncluster=True)
    _headlines = headlines(flats, returncluster=True)

    flats = doctextstyle.cluster.remove(flats, _text[1])
    flats = doctextstyle.cluster.remove(flats, _pagenumber[1])
    for item in _headlines[1]:
        flats = doctextstyle.cluster.remove(flats, item)

    def validator(item) -> bool:
        # Shrink footnotes to bottom area
        return item.bottom < 150 and item.length >= 25  # TODO:HOLY VALUE

    clustered = doctextstyle.cluster.cluster(
        flats,
        (doctextstyle.cluster.ClusterProperty.SIZE,),
        validator=validator,
        minsize=MIN_FOOTNOTES_COUNT,
        unique_content=True,
    )
    result = doctextstyle.cluster.bestmatch(clustered)
    return result


def paragraph(flats: doctextstyle.data.TextProperties):
    """Determine distance before and after a closed text block.

    This distance can be the distance to headlines, citation blocks and
    line endings.

    Hint: After may is the distance from last text line to footer
    start."""
    # TODO: REMOVE ITEMS WITH TEXT INDENTION, CAUSE THEY MAY ARE LIST ELEMENTS
    _text, _text_cluster = text(flats, returncluster=True)
    _text_before, _text_after = _text[3]

    before = []
    after = []
    for item in _text_cluster:
        if item.before is None:
            # page start
            continue
        if utila.near(item.before, _text_before, diff=1.5):
            # text line diff
            continue
        before.append(item.before)
    for item in _text_cluster:
        if item.after is None:
            # page number
            continue
        if utila.near(item.after, _text_after, diff=1.5):
            # text line diff
            continue
        after.append(item.after)

    before = hey.classificator.max_distance(before, diff=2.0)  # TODO: HOLY VAL
    after = hey.classificator.max_distance(after, diff=2.0)

    # most items in biggest cluster
    before = utila.modes(before[0].content)
    after = utila.modes(after[0].content)
    return before, after
