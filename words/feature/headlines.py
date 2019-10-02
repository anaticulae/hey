# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Example driven programming:

for chapter in document:
    for headline in chapter:
        p(headline)

Required resources:
    sections
    text
    font?

TODO: DO NOT MIX STRATEGYS

TODO: New concept:

Collect all title, cluster them by size and font distance and derivate the
headline level out of these information. Use further text information out of
headline.
"""

import serializeraw
import utila

import groupme.feature.numbers
import hey.textnavigator.navigator
import words.headlines.nolevel
import words.headlines.standard


@utila.checkdatatype
def work(
        sections: str,
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        sizeandborder: str,
        horizontals: str,
        boxes: str,
) -> str:
    """Extract headlines out of data

    Args:
        sections
        text
        text_position
        font_header
        sizeandborder
        horizontals
    """
    # prepare
    document = serializeraw.load_document(text)
    position = groupme.feature.numbers.load_textposition(text_position)
    sections = serializeraw.load_sections(sections)
    sizeandborder = serializeraw.load_pageborders(sizeandborder)
    horizontals = serializeraw.load_horizontals(horizontals)

    pagetextnavigators = hey.textnavigator.navigator.create_pagetextnavigators(
        text=document,
        text_positions=position,
    )
    fontstore = hey.fonts.store.create_fontstore(
        font_header,
        font_content,
    )

    strategies = [
        words.headlines.standard.StandardHeadlineExtractor,
        words.headlines.nolevel.NoLevelHeadlineExtractor,
    ]

    results = [
        strategy(
            sectionlist=sections,
            pagetextnavigators=pagetextnavigators,
            fontstore=fontstore,
            sizeandborder=sizeandborder,
            horizontals=horizontals,
            chapters=None,
        ).result() for strategy in strategies
    ]
    extracted = judge_result(results)
    # save
    dumped = serializeraw.dump_headlines(extracted)
    return dumped


def judge_result(results):
    # TODO: add judeging unit
    extracted = results[1]
    if any([len(item) for item in results[0]]):
        extracted = results[0]
    return extracted


SMALLEST_HEADLINE_SIZE = 1.1  # TODO: HOLY VALUE
SMALLEST_HEADLINE_DISTANCE = 1.05  # TODO:HOLY VALUE
SMALLEST_HEADLINE_DISTANCE_NOLEVEL = 1.1  # TODO:HOLY VALUE
