# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
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
import typing

import iamraw
import utila

import groupme.toc
import groupme.toc.group as gtg
import groupme.toc.strategy as gts
import groupme.toc.strategy.regex as gtsr
import hey.textnavigator.multiline as htm
import hey.textnavigator.navigator as htn


class GeometyRegexTocExtractor(gts.ExtractorStrategy):

    def result(self) -> gts.ExtractionResult:
        extracted = [analyse_page(item) for item in self.loaded.content]
        grouped = gtg.group(extracted)

        result = gts.ExtractionResult(content=grouped)
        return result


def analyse_page(content: htn.PageTextNavigator):
    assert htn.isnavigator(content), type(content)
    content = gts.remove_headline(content)
    grouped = group_areas(content)
    result = [parse_group(items) for items in grouped]
    return result


MIN_GROUP_GAP = 30.0  # TODO HOLY VALUE


def group_areas(content: htn.PageTextNavigator):
    # TODO: REMOVE AFTER FIXING PAGETEXTCONTENTNAVIGATOR
    content = [item for item in content if len(item.text.split(' ')) >= 2]
    linedistances = htm.linedistances(content, noneatend=False)
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


def parse_group(items) -> groupme.toc.TocLines:
    parsed = [gtsr.parse_line(item.text) for item in items]
    matched = [item is not None for item in parsed]
    if all(matched):
        return parsed
    result = []
    collected = []
    for match, item, parsed_item in zip(matched, items, parsed):
        if not match:
            collected.append(item)
            continue
        if match and collected:
            collected.append(item)
            extracted = group_collection_and_parse(collected)
            if extracted:
                result.append(extracted)
            else:
                # log not parsed
                utila.log('could not group and parse %s' % collected)
                assert 0
            collected = []
            continue
        result.append(parsed_item)
    if collected:
        result.append(collected)
    return result


def group_collection_and_parse(items):
    line = ' '.join([item.text for item in items])
    parsed = gtsr.parse_line(line)
    return parsed


BoundingBoxes = typing.List[iamraw.BoundingBox]


def group_boundings(items: BoundingBoxes, diff=10.0):
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
