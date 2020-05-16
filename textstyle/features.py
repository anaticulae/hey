# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import textstyle.cluster


def text(flats, returncluster: bool = False):
    clustered = textstyle.cluster.cluster(flats, (
        textstyle.cluster.ClusterProperty.SIZE,
        textstyle.cluster.ClusterProperty.FONT,
    ))
    result = textstyle.cluster.bestmatch(clustered)
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

    clustered = textstyle.cluster.cluster(
        flats,
        (
            textstyle.cluster.ClusterProperty.SIZE,
            textstyle.cluster.ClusterProperty.FONT,
        ),
        validator=validator,
    )
    # assert len(clustered) == 1, len(clustered)
    result = textstyle.cluster.bestmatch(clustered)
    if returncluster:
        return result, clustered[0] if clustered else []
    return result


def headlines(  # pylint:disable=R1260,R0914
        flats: textstyle.TextProperties,
        min_headline_count: int = 5,
        greater_than_text: bool = True,
        returncluster: bool = False,
):
    _text = text(flats, returncluster=True)
    _pagenumber = pagenumber(flats, returncluster=True)

    flats = textstyle.cluster.remove(flats, _text[1])
    flats = textstyle.cluster.remove(flats, _pagenumber[1])

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

    clustered = textstyle.cluster.cluster(
        flats,
        (textstyle.cluster.ClusterProperty.SIZE,),
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
        matched = textstyle.cluster.bestmatch(largest_font_size, number=index)  # pylint:disable=C0103
        if not matched:
            continue
        result.append(matched)
        result_cluster.append(largest_font_size[index].content)
    if returncluster:
        return result, result_cluster
    return result


MIN_FOOTNOTES_COUNT = 10  # TODO: HOLY VALUE


def footnote(flats: textstyle.TextProperties):
    _text = text(flats, returncluster=True)
    _pagenumber = pagenumber(flats, returncluster=True)
    _headlines = headlines(flats, returncluster=True)

    flats = textstyle.cluster.remove(flats, _text[1])
    flats = textstyle.cluster.remove(flats, _pagenumber[1])
    for item in _headlines[1]:
        flats = textstyle.cluster.remove(flats, item)

    def validator(item) -> bool:
        # Shrink footnotes to bottom area
        return item.bottom < 150 and item.length >= 25  # TODO:HOLY VALUE

    clustered = textstyle.cluster.cluster(
        flats,
        (textstyle.cluster.ClusterProperty.SIZE,),
        validator=validator,
        minsize=MIN_FOOTNOTES_COUNT,
        unique_content=True,
    )
    result = textstyle.cluster.bestmatch(clustered)
    return result
