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


def decide(clustered, fontstore, pagecount) -> iamraw.DocTextStyle:
    # avoid side effects
    clustered = clustered[:]

    # determine text chunk
    text = largest(clustered)
    text_size, text_distance, text_family = decide_text(text)
    clustered = remove_cluster(clustered, [text])
    # determine headlines
    headlines, fonts, befores, afters, removes = dvh.decide_headlines(
        clustered,
        pagecount=pagecount,
    )
    clustered = remove_cluster(clustered, removes)

    result = iamraw.DocTextStyle(
        text_size=text_size,
        text_distance=text_distance,
        text_family=fontstore[text_family].name,
        h1_size=headlines[0],
        h2_size=headlines[1],
        h3_size=headlines[2],
        h4_size=headlines[2],
        h1_family=fontstore[fonts[0]].name if fonts[0] else None,
        h2_family=fontstore[fonts[1]].name if fonts[1] else None,
        h3_family=fontstore[fonts[2]].name if fonts[2] else None,
        h4_family=fontstore[fonts[3]].name if fonts[3] else None,
        h1_before=befores[0],
        h2_before=befores[1],
        h3_before=befores[2],
        h4_before=befores[3],
        h1_after=afters[0],
        h2_after=afters[1],
        h3_after=afters[2],
        h4_after=afters[3],
    )
    return result


def decide_text(text):
    # TODO: USE MOST COMMON SIZE
    first = text[0][0].style
    return first.textsize(), -1, first.fontid


def remove_cluster(cluster, removes):
    removes = {hash(str(item)) for item in removes}
    # remove cluster
    result = [item for item in cluster if hash(str(item)) not in removes]
    return result


def largest(items) -> 'Cluster':
    if not items:
        raise ValueError('empty collection')
    longest = items[0]
    for item in items[1:]:
        if len(item) < len(longest):
            continue
        longest = item
    return longest
