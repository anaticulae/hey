# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""table of content - geometry regex strategy
==========================================

Use the geometry of the page to extract the table of content.

Strategy:

* split area by `MIN_GROUP_GAP`
    * run regex for every item in group
    * group items which not pass the parser
    * run parser on grouped items
* merge extracted groups to get table of content over pages
* validate extracted toc

"""
import collections

import iamraw
import texmex
import utila

import groupme.toc.strategy
import groupme.toc.strategy.utils

MIN_GROUP_GAP = 30.0  # TODO HOLY VALUE


class GeometryRegexTocExtractor(groupme.toc.strategy.ExtractorStrategy):

    def result(self) -> groupme.toc.strategy.ExtractionResult:
        extracted = [analyse_page(item) for item in self.loaded.content]
        flat = utila.flatten(utila.flatten(extracted))

        valid = groupme.toc.strategy.remove_nonconnected_tocs(flat)

        grouped = groupme.toc.strategy.group(valid)
        invalid = [item for item in flat if item not in valid]

        result = groupme.toc.strategy.ExtractionResult(
            content=grouped.content,
            invalid=invalid,
        )
        assert isinstance(result.content, list), type(result.content)
        return result


def analyse_page(content: texmex.PageTextNavigator):
    assert isinstance(content, texmex.NavigatorMixin), type(content)
    content = groupme.toc.strategy.remove_headline(content)
    grouped = group_areas(content)
    result = [
        groupme.toc.strategy.utils.parse_group(items, content.page)
        for items in grouped
    ]
    # remove not parsed
    result = [item for item in result if item]

    # set page where toc was parsed
    for group in result:
        for item in group:
            item.raw_location = content.page
    return result


def group_areas(content: texmex.PageTextNavigator):
    linedistances = texmex.linedistances(content, noneatend=False)
    result = []
    grouped = []
    for item, distance in zip(content, linedistances):
        grouped.append(item)
        if distance > MIN_GROUP_GAP:
            result.append(grouped)
            grouped = []
    # add last one, cause last one has no linedistance
    grouped.append(content[-1])
    if grouped:
        result.append(grouped)
    return result


def group_boundings(items: iamraw.BoundingBoxes, diff=10.0):
    assert diff >= 1.0, 'diff to low'
    counter = collections.defaultdict(int)
    for bounding in items:
        width = bounding.x1 - bounding.x0
        index = int(width / diff)
        counter[index] += 1

    result = [(key * diff, value) for key, value in counter.items()]

    result = sorted(result, key=lambda x: x[1], reverse=True)
    return result


def group_items(items, diff=10.0):
    assert diff > 0.0, 'diff to low'
    counter = collections.defaultdict(int)
    for item in items:
        index = int(item / diff)
        counter[index] += 1

    result = [
        (utila.roundme(key * diff), value) for key, value in counter.items()
    ]
    result = sorted(result, key=lambda x: x[1], reverse=True)
    return result
