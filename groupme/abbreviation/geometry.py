# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Parser: Geometry Strategy
======================================

This approach splits the page in two columns and detect a left shortcut
and a right description column. It is required that the distance between
left and right column is not ?too? tight.

Working Examples
----------------

* bachelor37: page 2

Not working
-----------

* homework50: columns are to tight together

Nearly working
--------------

* master116: improve layout parser
"""

import configo
import iamraw
import texmex
import utila
import utila.math

import groupme.abbreviation


class GeometryAbbreviationParser(groupme.abbreviation.AbbreviationExtractorStrategy): # yapf:disable

    def result(self) -> iamraw.AbbreviationResult:
        ready = iamraw.AbbreviationResult()
        for page in self.loaded.normal:
            parsed = parse_page(page)
            if parsed is None:
                utila.info(f'could not parse page: {page.page}')
                continue
            for item in parsed:
                ready.append(item)
        return ready


def parse_page(page) -> iamraw.Abbreviations:
    line_gaps = lines(page)
    if not line_gaps:
        utila.debug(f'no linegap on page {page.page}')
        # distance between pages is to small. See MIN_LINE_GAP
        return []
    marker = columns(page)

    if not marker:
        return None

    short_marker = marker[0]
    description_marker = marker[1]
    short_column = column_data(page, short_marker)
    description_column = column_data(page, description_marker)

    if overlapping_column(short_column, description_column):
        # TODO: EXTEND ERROR MESSAGE
        utila.debug('could not analyze, columns are mixed/ambigous')
        return None
    adjusted = adjust_columns(
        short_column,
        description_column,
        line_gaps,
        short_marker,
    )
    if adjusted is None:
        return None
    left, right = adjusted
    result = []
    for short, description in zip(left, right):
        description = [item.text.strip() for item in description]
        description = ' '.join(description)
        result.append(
            iamraw.Abbreviation(
                short=short.text.strip(),
                description=description,
            ))
    return result


def overlapping_column(short, description):
    # TODO: INTRODUCE HASH BOUNDING METHOD
    shorts = set(str(item.bounding) for item in short)
    descriptions = set(str(item.bounding) for item in description)

    mixig = shorts & descriptions
    return mixig


def adjust_columns(short_column, description_column, line_gaps, short_marker):
    """Adjust multi line columns. Group right side items to
    corresponding left side shortcut."""
    inside_all = all_columns([short_column, description_column])
    left = [
        item for item in inside_all
        if utila.near(item.bounding[0], short_marker)
    ]
    right = []
    for first, second in zip(left[:-1], left[1:]):
        start, end = first.bounding[1], second.bounding[1]
        start = start - 5.0  # TODO: HOLY VALUE, give some tolerance
        right.append([
            item for item in description_column
            if start <= item.bounding[1] <= item.bounding[3] <= end
        ])
    if not left or not right:
        # could not adjust multiline colum
        return None

    # TODO: DIRTY, move to separate method
    # group last item
    start = left[-1].bounding[1]
    if len(line_gaps) >= 2:
        # biggest item is distance between multiline shortcut lines
        # second biggest item is normal line distance
        max_gap = line_gaps[1]
    else:
        # only single lines, no multiline shortcut lines
        max_gap = line_gaps[0]
    last = []
    for item in description_column:
        if item.bounding[1] < start:
            continue
        if (item.bounding[1] - start) > max_gap:
            # gap after content is to big
            break
        last.append(item)
        start = item.bounding[3]
    right.append(last)
    assert len(left) == len(right), 'could not parse both columns correctly'
    return left, right


def all_columns(items):
    """Select items which have a correspondet in every column with the
    same y1-baseline.

    Using y1 to use `baseline` of text cause lower z and upper Z have
    same base but the top coordinate can vary very much."""
    buckets = [set() for _ in items]
    for index, column_ in enumerate(items):
        for item in column_:
            rounded = utila.roundme(item.bounding[3], digits=0)
            # TODO: DIRTY :)
            buckets[index].add(rounded + 4.0)
            buckets[index].add(rounded + 3.0)
            buckets[index].add(rounded + 2.0)
            buckets[index].add(rounded + 1.0)
            buckets[index].add(rounded)
            buckets[index].add(rounded - 1.0)
            buckets[index].add(rounded - 2.0)
            buckets[index].add(rounded - 3.0)
            buckets[index].add(rounded - 4.0)
    result = []
    all_items = utila.flatten(items)
    for item in all_items:
        rounded = utila.roundme(item.bounding[3], digits=0)
        inside = [rounded in bucket for bucket in buckets]
        if not all(inside):
            continue
        if len([it for it in inside if it]) < 2:
            continue
        result.append(item)
    return result


# TODO: THIS HIGH DIFF IS REQUIRED FOR BACHELOR37 EXAMPLE, BECAUSE HIDDEN
# WHITESPACES MAKES ANALYSIS COMPLICATED -> TODO: IMPROVE PARSER
def column_data(page, x0, diff: float = 60.0):
    """Filter items by x0 coordinate. Find items which are on a vertical
    line."""
    result = []
    for item in page:
        if not utila.near(item.bounding[0], x0, diff):
            continue
        result.append(item)
    return result


def columns(page) -> utila.Numbers:
    """Sort columns from left to right."""
    collected = []
    for item in page:
        x0 = item.bounding[0]
        collected.append(x0)

    clustered = utila.max_distance(
        collected,
        diff=2.0,  # TODO: HOLY VALUE
        min_elements=5  # TODO: HOLY VALUE
    )
    if len(clustered) < 2:
        return None

    result = [item[0] for item in clustered]
    result = sorted(result)
    return result


MIN_LINE_GAP = configo.HV_FLOAT_PLUS(10.0)


def lines(page) -> utila.Numbers:
    line_distance = texmex.linedistances(
        page,
        noneatend=False,
    )
    clustered = utila.max_distance(
        line_distance,
        diff=2.0,  # TODO: HOLY VALUE
        min_elements=5  # TODO: HOLY VALUE
    )
    result = [item[0] for item in clustered if item[0] >= MIN_LINE_GAP]
    # huggest element first
    result = sorted(result, reverse=True)
    return result
