# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import hey.path
import hey.textnavigator
import hey.textnavigator.fonts
import hey.utils

# Merge lines with lower distance to one text chunk.
MAX_MERGE_DISTANCE = configo.HV_FLOAT_PLUS(default=3.55).value
MAX_MERGE_HORIZONTALY = configo.HV_FLOAT_PLUS(default=14.0).value


def merge_content(
        text: hey.textnavigator.TextBoundsList,
        max_x_merge=MAX_MERGE_HORIZONTALY,
        max_y_merge=MAX_MERGE_DISTANCE,
        uindex=None,
) -> hey.textnavigator.TextBoundsList:
    """Merge content blocks to create greater content blocks depending on
    merge strategy.

    Args:
        text: chunk with iamraw.BoundingBox to merge
        max_x_merge(float): feed distance between the two left sides
        max_y_merge(float): vertical distance between 2 BoundingBoxes to
                            merge them into one
        uindex(list[int]): undefined index to link text(TextBoundsList) with
                           text-source if uindex is None, the `uindex` is an
                           ascending list starting with zero.
    Returns:
        (result, merged) - result is the merged content, merged - stores the
                           uindex which are merged together
    """
    if not text:
        # Nothing to merge
        return []

    # ensure input
    assert all([
        isinstance(item, hey.textnavigator.TextBoundsInfo) for item in text
    ]), str(text)

    uindex = list(range(len(text))) if uindex is None else uindex
    bounds = [item.bounds for item in text]
    font_distance = hey.textnavigator.fonts.fontdistance(bounds)
    feed_distance = hey.textnavigator.fonts.feeddistance(bounds)

    # copy element
    result = [(text[0].bounds, [text[0].text])]
    merged = [[uindex[0]]]
    lines = zip(font_distance, feed_distance)
    for index, (fontdist, feeddist) in enumerate(lines, start=1):
        current_bounds, current_text = text[index].bounds, text[index].text
        if fontdist > max_y_merge:
            # new entree
            result.append((current_bounds, [current_text]))
            merged.append([uindex[index]])
            continue
        if abs(feeddist) > max_x_merge:
            # new entree
            result.append((current_bounds, [current_text]))
            merged.append([uindex[index]])
            continue

        # Merge me
        member_location, member_content = result[-1]
        merger_location, merger_content = text[index].bounds, text[index].text
        member_content.append(merger_content)
        merged[-1].append(uindex[index])
        # merged items together and save them as last item
        result[-1] = (
            iamraw.common_box([member_location, merger_location]),
            member_content,
        )

    result = [
        hey.textnavigator.TextBoundsInfo(
            text=item[1],
            bounds=item[0],
        ) for item in result
    ]
    return result, merged


def merge_content_join(result):
    result = [
        hey.textnavigator.TextBoundsInfo(
            text=utila.NEWLINE.join(item.text),
            bounds=item.bounds,
        ) for item in result
    ]
    return result
