# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import configo
import iamraw
import texmex


def split(content):
    # Split by highnotes at start of line content
    result = []
    collected = []
    for line in content:
        first = line.style.content[0].rise
        if first > 4.0 and collected:
            joined = '\n'.join([item.text for item in collected])
            result.append(joined)
            collected = []
        collected.append(line)
    if collected:
        joined = '\n'.join([item.text for item in collected])
        result.append(joined)
    return result


VERTICAL_LINE_DIFF_OF_HIGHNOTES = configo.HV_FLOAT_PLUS(default=15.0).value

HIGHNOTE_MIN_RISE = configo.HV_FLOAT_PLUS(default=3.0).value


def split_textinfo(content) -> list:
    """Split text by `hightnote` and preserve TextInfo.

    Returns:
        list of a tuple of highnote and content
    """
    assert isinstance(content, list), type(content)
    result = []
    highnote = None
    collected = []
    for item in content:
        for style in item.style.content:
            if style.rise >= HIGHNOTE_MIN_RISE:
                if highnote:
                    result.append((highnote, union(collected)))
                    collected = []
                style = style.copy()
                highnote = texmex.TextInfo(
                    text=item.text[style.start:style.end],
                    style=style,
                    bounding=char_bounding(item.bounding, item.text, style),
                )
                style.start = 0
                style.end = len(highnote.text)
            else:
                collected.append((item.text, style))
    if highnote:
        # ?THERE IS ALWAYS A REST?
        result.append((highnote, union(collected)))
    return result


def merge_online(items) -> list:
    """Ensure that high notes are located on a vertical line. Therefore
    we have to ignore highnotes which are located inside the text and
    not part of the text flow.

    Steps:
        1. Determine the most left highnotes
        2. Adjust highnotes on most left one
        3. Merge other highnotes into text
    """
    if not items:
        return []
    result = []
    mostleft = min([item.bounding.x0 for item, _ in items])
    high, collected = None, []
    for highnote, content in items:
        diff = math.fabs(highnote.bounding.x0 - mostleft)
        if diff > VERTICAL_LINE_DIFF_OF_HIGHNOTES:
            # highnote in content
            collected.append(shrink_tostyle(highnote.text, highnote.style))
            collected.extend([
                shrink_tostyle(content.text, style) for style in content.style
            ])
        else:
            # new highnotes
            if high:
                result.append((high, union(collected)))
            high = highnote
            collected = [
                shrink_tostyle(content.text, style) for style in content.style
            ]
    result.append((high, union(collected)))
    return result


def shrink_tostyle(text, style):
    text = text[style.start:style.end]
    style = style.copy()
    style.start = 0
    style.end = len(text)
    return text, style


def union(items) -> texmex.TextInfo:
    raw = ''
    content = []
    for (text, style) in items:
        start = len(raw)
        raw += text[style.start:style.end]
        end = len(raw)
        section_style = style.copy()
        section_style.start, section_style.end = start, end
        content.append(section_style)
    result = texmex.TextInfo(
        text=raw,
        style=texmex.TextStyle(content=content),
    )
    return result


def char_bounding(
        bounding: iamraw.BoundingBox,
        text: str,
        style: texmex.TextStyle,
) -> iamraw.BoundingBox:
    width = bounding.x1 - bounding.x0
    char_width = width / len(text)
    x0 = bounding.x0 + char_width * style.start
    x1 = bounding.x0 + char_width * style.end
    result = iamraw.BoundingBox(x0, bounding.y0, x1, bounding.y1)
    return result
