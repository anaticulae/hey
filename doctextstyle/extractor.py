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
import utila

import doctextstyle
import doctextstyle.features
import doctextstyle.features.content
import doctextstyle.features.pagesize
import doctextstyle.features.textbounding as dtt
import doctextstyle.parser
import doctextstyle.utils
import groupme.path


def extract(path: str, pages: tuple = None) -> doctextstyle.data.DocTextStyle:  # pylint:disable=R0914,R0915
    navigator = serializeraw.create_pagetextnavigators_frompath(
        path,
        prefix='oneline',
        pages=pages,
    )
    try:
        cnavigator = serializeraw.create_pagetextcontentnavigators_frompath(
            path,
            prefix='oneline',
            pages=pages,
        )
    except FileNotFoundError as error:
        cnavigator = None
        utila.error(f'missing page text content navigator: {error}')

    parsed = doctextstyle.parser.parses(navigator)
    flat = doctextstyle.utils.flatten(parsed)

    text = doctextstyle.features.text(flat)
    text_after = text[3][1]

    result = doctextstyle.data.DocTextStyle(
        text_size=text[0],
        text_distance=text_after,
        text_family=text[1],
    )

    extract_headlines(result, flat)

    pagenumber = doctextstyle.features.pagenumber(flat)
    if pagenumber:
        result.pagenumber_size = pagenumber[0]
        result.pagenumber_family = pagenumber[1]

    extract_footnotes(result, flat)

    pagesizes = doctextstyle.features.pagesize.pagesizes(path, pages=pages)
    result.page_width, result.page_height = pagesizes[0][0]
    with contextlib.suppress(IndexError):
        result.page_rotated_width, result.page_rotated_height = pagesizes[1][0]

    extract_contentborder(result, path, pages)

    extract_textdimension(result, cnavigator)
    return result


def extract_footnotes(result, flat):
    footnotes = doctextstyle.features.footnote(flat)
    if footnotes:
        footnote_after = footnotes[3][1]
        result.footnote_size = footnotes[0]
        result.footnote_family = footnotes[1]
        result.footnote_distance = footnote_after


def extract_contentborder(result, path, pages):
    leftright = groupme.path.border_leftright(path)
    content = doctextstyle.features.content.content(leftright, pages=pages)
    if content:
        normal = content[0][0]
        result.content_left = normal[0]
        result.content_right = normal[1]
        result.content_top = normal[2]
        result.content_bottom = normal[3]
    if len(content) > 1:
        rotated = content[1][0]
        result.content_rotated_left = rotated[0]
        result.content_rotated_right = rotated[1]
        result.content_rotated_top = rotated[2]
        result.content_rotated_bottom = rotated[3]


def extract_headlines(result, flat):
    headlines = doctextstyle.features.headlines(flat)
    if not headlines:
        return

    result.h1_size = headlines[0][0]
    result.h1_family = headlines[0][1]
    result.h1_before = headlines[0][3][0]
    result.h1_after = headlines[0][3][1]

    if len(headlines) == 1:
        return
    result.h2_size = headlines[1][0]
    result.h2_family = headlines[1][1]
    result.h2_before = headlines[1][3][0]
    result.h2_after = headlines[1][3][1]

    if len(headlines) == 2:
        return
    result.h3_size = headlines[2][0]
    result.h3_family = headlines[2][1]
    result.h3_before = headlines[2][3][0]
    result.h3_after = headlines[2][3][1]


def extract_textdimension(result, cnavigators):
    if not cnavigators:
        return
    twidth = dtt.text_width(cnavigators)
    twidth_min = dtt.text_width_min(cnavigators)
    twidth_max = dtt.text_width_max(cnavigators)
    result.text_width = twidth
    result.text_width_min = twidth_min
    result.text_width_max = twidth_max
