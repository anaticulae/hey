# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import doctextstyle.cluster

MIN_HEADLINE_CLUSTER_SIZE = configo.HV_INT_PLUS(3).value
MIN_HEADLINE_LENGTH = configo.HV_INT_PLUS(7).value


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


DEFAULT_DISTANCE_BEFORE_TEXT = configo.HV_FLOAT_PLUS(18.0).value
DEFAULT_DISTANCE_AFTER_TEXT = configo.HV_FLOAT_PLUS(18.0).value


def headlines(  # pylint:disable=R1260,R0914
        flats: iamraw.TextProperties,
        min_headline_count: int = None,
        min_headline_length: int = None,
        greater_than_text: bool = True,
        returncluster: bool = False,
):
    if min_headline_count is None:
        min_headline_count = MIN_HEADLINE_CLUSTER_SIZE
    if min_headline_length is None:
        min_headline_length = MIN_HEADLINE_LENGTH

    _text = text(flats, returncluster=True)
    _pagenumber = pagenumber(flats, returncluster=True)

    flats = doctextstyle.cluster.remove(flats, _text[1])
    flats = doctextstyle.cluster.remove(flats, _pagenumber[1])

    textsize = _text[0][0]
    distance_before_textsize, distance_after_textsize = _text[0][3]

    if distance_before_textsize is None:
        utila.error('distance before `textsize` is None; '
                    'disable headline detection feature')
    if distance_after_textsize is None:
        utila.error('distance after  `textsize` is None;'
                    ' disable headline detection feature')

    if distance_before_textsize is None or distance_after_textsize is None:
        # disable strategy
        return []

    if greater_than_text:
        flats = [item for item in flats if item.size >= textsize]

    # remove too short text chuncks which are not possible headlines
    flats = [item for item in flats if item.length >= MIN_HEADLINE_LENGTH]

    def valid_headline(item) -> bool:  # pylint:disable=R0911
        if item.before is None:
            return True
        if item.before <= distance_before_textsize * 1.2:  # TODO: HOLY VALUE
            return False
        if item.after is None:
            return False
        if item.after <= distance_after_textsize * 1.2:  # TODO: HOLY VALUE
            return False
        return True

    clustered = doctextstyle.cluster.cluster(
        flats,
        (doctextstyle.cluster.ClusterProperty.FONT,),
        validator=valid_headline,
        minsize=min_headline_count,
        unique_content=True,  # remove duplicated footer/header content
    )

    clustered = validate_headline_cluster(clustered)

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
MIN_HEADLINE_SPREAD = configo.HV_PERCENT_PLUS(50).value


def validate_headline_cluster(clusters):
    """Check that detected headline style is spread over the document
    and not located on few pages. Lower spreads indicates that more than
    one line on a page is detected as headline, which indicates false
    detection."""

    def valid(cluster) -> bool:
        """\
        Returns:
            1 5 8 10    valid/True     : 1.0   5/5
            1 1 1 2 2   invalid/False  : 0.4   2/5
        """
        pages = utila.make_unique([item.page for item in cluster])
        ratio = len(pages) / len(cluster)
        return ratio >= MIN_HEADLINE_SPREAD

    result = [cluster for cluster in clusters if valid(cluster)]
    return result


def footnote(flats: iamraw.TextProperties):
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
        max_size_diff=doctextstyle.cluster.NO_TOLERANCE,
        max_before_diff=doctextstyle.cluster.NO_TOLERANCE,
        max_after_diff=doctextstyle.cluster.NO_TOLERANCE,
    )
    result = doctextstyle.cluster.bestmatch(clustered)
    return result


def paragraph(flats: iamraw.TextProperties, digits: int = 1):
    """Determine distance before and after a closed text block.

    This distance can be the distance to headlines, citation blocks and
    line endings.

    Hint: In some cases `after` defines the distances from the last text
    line to the footer start.
    """
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

    before = utila.roundme(before, digits=digits, convert=False)  # pylint:disable=R0204
    after = utila.roundme(after, digits=digits, convert=False)  # pylint:disable=R0204

    before = utila.max_distance(before, diff=2.0)  # TODO: HOLY VAL
    after = utila.max_distance(after, diff=2.0)

    # most items in biggest cluster
    before = utila.modes(before[0].content)
    after = utila.modes(after[0].content)
    return before, after
