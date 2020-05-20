# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import serializeraw

import doctextstyle
import doctextstyle.features
import doctextstyle.features.pagesize
import doctextstyle.parser
import doctextstyle.utils


def extract(path: str, pages: tuple = None) -> doctextstyle.data.DocTextStyle:
    loaded = serializeraw.create_pagetextnavigators_frompath(
        path,
        prefix='oneline',
        pages=pages,
    )
    parsed = doctextstyle.parser.parses(loaded)
    flat = doctextstyle.utils.flatten(parsed)

    text = doctextstyle.features.text(flat)
    text_after = text[3][1]

    result = doctextstyle.data.DocTextStyle(
        text_size=text[0],
        text_distance=text_after,
        text_family=text[1],
    )

    pagenumber = doctextstyle.features.pagenumber(flat)
    if pagenumber:
        result.pagenumber_size = pagenumber[0]
        result.pagenumber_family = pagenumber[1]

    footnotes = doctextstyle.features.footnote(flat)
    if footnotes:
        footnote_after = footnotes[3][1]
        result.footnote_size = footnotes[0]
        result.footnote_family = footnotes[1]
        result.footnote_distance = footnote_after

    headlines = doctextstyle.features.headlines(flat)
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

    pagesizes = doctextstyle.features.pagesize.pagesizes(path, pages=pages)
    result.page_width, result.page_height = pagesizes[0][0]
    with contextlib.suppress(IndexError):
        result.page_rotated_width, result.page_rotated_height = pagesizes[1][0]
    return result
