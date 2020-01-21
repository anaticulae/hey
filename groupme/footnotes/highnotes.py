# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


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
