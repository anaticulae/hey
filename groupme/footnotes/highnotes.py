# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hey.textnavigator.style


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


def split_textinfo(content):
    """Split text by `hightnote` and preserve TextInfo.

    Yields:
        tuple: of highnote and content
    """
    assert isinstance(content, list), type(content)
    highnote = None
    collected = []
    for item in content:
        for style in item.style.content:
            if style.rise >= 5.0:
                if highnote:
                    yield highnote, union(collected)
                    collected = []
                highnote = hey.textnavigator.style.TextInfo(
                    text=item.text[style.start:style.end],
                    style=style,
                )
            else:
                collected.append((item.text, style))
    if highnote:
        yield highnote, union(collected)


def union(items) -> hey.textnavigator.style.TextInfo:
    raw = ''
    content = []
    for (text, style) in items:
        start = len(raw)
        raw += text[style.start:style.end]
        end = len(raw)
        section_style = style.copy()
        section_style.start, section_style.end = start, end
        content.append(section_style)
    result = hey.textnavigator.style.TextInfo(
        text=raw,
        style=hey.textnavigator.style.TextStyle(content=content),
    )
    return result
