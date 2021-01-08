# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import elements
import iamraw
import utila

import doctextstyle.cluster
import doctextstyle.features
import doctextstyle.utils

MIN_HEADLINE_CLUSTER_SIZE = configo.HV_INT_PLUS(3).value
MIN_HEADLINE_LENGTH = configo.HV_INT_PLUS(7).value


def headlines(  # pylint:disable=R1260,R0914
        flats: iamraw.TextProperties,
        *,
        min_headline_count: int = None,
        min_headline_length: int = None,
        greater_than_text: bool = True,
        headline_start: bool = True,
        returncluster: bool = False,
):
    if min_headline_count is None:
        min_headline_count = MIN_HEADLINE_CLUSTER_SIZE
    if min_headline_length is None:
        min_headline_length = MIN_HEADLINE_LENGTH

    _text = doctextstyle.features.text(flats, returncluster=True)
    if not _text:
        # too few data
        return []
    _pagenumber = doctextstyle.features.pagenumber(flats, returncluster=True)

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
        if elements.noheadline(item.hashed):
            return False
        if elements.isheadline(item.hashed):
            return True
        if item.before is None:
            if doctextstyle.utils.headline_blacklisted(item.hashed):
                # Kapitel 1 at the start of the page followed by title
                return False
            return True
        if item.after is None:
            return False
        if item.before <= distance_before_textsize * 1.2:  # TODO: HOLY VALUE
            return False
        # TODO: INTRODUCE NEW STRATEGY FOR HEADLINES WITHOUT HUGE DISTANCE
        if item.after < distance_after_textsize * 0.98:  # TODO: HOLY VALUE
            return False
        if item.hashed.count('.') > 5:  # TODO: HOLY VALUE
            # filter table items
            # DISKUSSION ................ 36
            return False
        return True

    selection = (
        doctextstyle.cluster.ClusterProperty.FONT,
        doctextstyle.cluster.ClusterProperty.LEFT,
    ) if headline_start else (doctextstyle.cluster.ClusterProperty.FONT,)

    clustered = doctextstyle.cluster.cluster(
        flats,
        selection=selection,
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
