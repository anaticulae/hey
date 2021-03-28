# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import doctextstyle.vector.headlines as dvh


def decide(clustered, fontstore) -> iamraw.DocTextStyle:
    notempty = [item for item in clustered if len(item)]
    text_ = largest(notempty)
    notempty = notempty[0:text_] + notempty[text_:]
    text = notempty[text_]
    text_size, text_distance, text_family = decide_text(text)
    headlines, deletes = dvh.decide_headlines(notempty)
    deletes = {hash(str(item)) for item in deletes}
    notempty = [item for item in notempty if hash(str(item)) not in deletes]

    result = iamraw.DocTextStyle(
        text_size=text_size,
        text_distance=text_distance,
        text_family=fontstore[text_family].name,
        h1_size=headlines[0],
        h2_size=headlines[1],
        h3_size=headlines[2],
        h4_size=headlines[2],
    )
    return result


def decide_text(text):
    first = text[0].style
    return first.textsize(), -1, first.fontid


def largest(items) -> int:
    if not items:
        raise ValueError('empty collection')
    longest = 0
    for index, item in enumerate(items[1:], start=1):
        if len(item) < len(items[longest]):
            continue
        longest = index
    return longest
