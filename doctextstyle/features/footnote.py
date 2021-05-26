# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

import doctextstyle.cluster
import doctextstyle.features
import doctextstyle.features.headline

MIN_FOOTNOTES_COUNT = 10  # TODO: HOLY VALUE


def footnote(flats: iamraw.TextProperties):
    _text = doctextstyle.features.text(flats, returncluster=True)
    _pagenumber = doctextstyle.features.pagenumber(flats, returncluster=True)
    _headlines = doctextstyle.features.headline.headlines(flats,
                                                          returncluster=True)

    if _text:
        flats = doctextstyle.cluster.remove(flats, _text[1])
    else:
        utila.debug('footnote: no text style')

    if _pagenumber:
        flats = doctextstyle.cluster.remove(flats, _pagenumber[1])
    else:
        utila.debug('footnote: no pagenumber style')

    if _headlines:
        for item in _headlines[1]:
            flats = doctextstyle.cluster.remove(flats, item)
    else:
        utila.debug('footnote: no headline style')

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
