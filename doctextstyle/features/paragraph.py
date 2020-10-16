# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

import doctextstyle.features


def paragraph(flats: iamraw.TextProperties, digits: int = 1):
    """Determine distance before and after a closed text block.

    This distance can be the distance to headlines, citation blocks and
    line endings.

    Hint: In some cases `after` defines the distances from the last text
    line to the footer start.
    """
    # TODO: REMOVE ITEMS WITH TEXT INDENTION, CAUSE THEY MAY ARE LIST ELEMENTS
    _text, _text_cluster = doctextstyle.features.text(flats, returncluster=True)
    _text_before, _text_after = _text[3]

    before = []
    after = []
    for item in _text_cluster:
        if item.before is None:
            # page start
            continue
        if utila.near(item.before, _text_before, diff=1.5):
            # text line diff
            continue
        before.append(item.before)
    for item in _text_cluster:
        if item.after is None:
            # page number
            continue
        if utila.near(item.after, _text_after, diff=1.5):
            # text line diff
            continue
        after.append(item.after)

    before = utila.roundme(before, digits=digits, convert=False)  # pylint:disable=R0204
    after = utila.roundme(after, digits=digits, convert=False)  # pylint:disable=R0204

    before = utila.max_distance(before, diff=2.0)  # TODO: HOLY VAL
    after = utila.max_distance(after, diff=2.0)

    # most items in biggest cluster
    before = utila.modes(before[0].content)
    after = utila.modes(after[0].content)
    return before, after
