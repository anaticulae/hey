# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import textstyle
import textstyle.features


def extract(path: str, pages: tuple = None) -> textstyle.DocTextStyle:
    loaded = serializeraw.create_pagetextnavigators_frompath(
        path,
        prefix='oneline',
        pages=pages,
    )
    parsed = textstyle.parser.parses(loaded)
    flat = textstyle.utils.flatten(parsed)

    text = textstyle.features.text(flat)
    text_after = text[3][1]

    result = textstyle.DocTextStyle(
        text_size=text[0],
        text_distance=text_after,
        text_family=text[1],
    )

    pagenumber = textstyle.features.pagenumber(flat)
    if pagenumber:
        result.pagenumber_size = pagenumber[0]
        result.pagenumber_family = pagenumber[1]

    footnotes = textstyle.features.footnote(flat)
    if footnotes:
        footnotes_after = footnotes[3][1]
        result.footnotes_size = footnotes[0]
        result.footnotes_family = footnotes[1]
        result.footnotes_distance = footnotes_after

    headlines = textstyle.features.headlines(flat)
    if headlines:
        result.h1_size = headlines[0][0]
        result.h1_family = headlines[0][1]
        result.h1_before = headlines[0][3][0]
        result.h1_after = headlines[0][3][1]
        if len(headlines) >= 2:
            result.h2_size = headlines[1][0]
            result.h2_family = headlines[1][1]
            result.h2_before = headlines[1][3][0]
            result.h2_after = headlines[1][3][1]
        if len(headlines) >= 3:
            result.h3_size = headlines[2][0]
            result.h3_family = headlines[2][1]
            result.h3_before = headlines[2][3][0]
            result.h3_after = headlines[2][3][1]

    return result
