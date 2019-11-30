# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""table of content - geometry strategy
====================================
"""

import utila

import groupme.toc.group as gtg
import groupme.toc.strategy as gts
import hey.textnavigator.fonts as htf
import hey.textnavigator.navigator as htn

MAX_HEADLINE_LEVEL = 3  # TODO: HOLY VALUE

MAX_HEADLINE_HEIGHT = 20  # TODO: HOLY VALUE


class GeometryTocExtractor(gts.ExtractorStrategy):

    def result(self) -> gts.ExtractionResult:
        extracted = []
        feed = sorted(
            htf.document_textfeed(
                self.loaded.content,
                count=MAX_HEADLINE_LEVEL,
            ))
        for page in self.loaded.content:
            analyzed = analyse_page(page, feed)
            extracted.extend(analyzed)

        grouped = group_areas(extracted)
        import groupme.toc.strategy.georegex as gtsg
        content = [gtsg.parse_group(group) for group in grouped]

        result = gts.ExtractionResult(content=content)
        return result


def analyse_page(navigator: htn.PageTextContentNavigators, level_feed: list):
    result = []
    textbounds = htf.textbounds(navigator, navigator.content)
    for item in textbounds:
        if item.text in ('Inhaltsverzeichnis', 'Contents'):
            continue
        current_level = level(item.bounds.xdist, level_feed)
        result.append((current_level, item))
    return result


def group_areas(items):
    result = []
    current = []
    for level_, item in items:
        if level_ == 0 and current:
            # new group
            result.append(current)
            current = []
            # continue
        current.append(item)
    if current:
        result.append(current)
    return result


def level(xdist, levels):
    for index, item in enumerate(levels):
        if xdist <= item:
            return index
    return None
