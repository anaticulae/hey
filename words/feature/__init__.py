# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import serializeraw

import hey.fonts.store
import hey.textnavigator.navigator
import words.boxed
import words.headlines


def load_resources(
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        headlines: str,
        pagesizes: str,
        boxes: str,
        headerfooters: str,
        pages=None,
):
    """Load content from path and create required object"""
    text = serializeraw.load_document(text, pages=pages)
    position = serializeraw.load_textpositions(text_position, pages=pages)
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    boxes = serializeraw.load_boxes(boxes, pages=pages)
    fontstore = hey.fonts.store.create_fontstore(font_header, font_content)
    textnavigators = hey.textnavigator.navigator.create_pagetextnavigators(
        text=text,
        text_positions=position,
    )
    contentborder = serializeraw.load_pageborders(pagesizes, pages=pages)
    headerfooters = serializeraw.load_headerfooter(
        headerfooters,
        pages=pages,
    )
    # contentborder = [(item.border, item.page) for item in contentborder]
    border = words.headlines.contentborder(
        contentborder,
        headerfooters,
    )
    boxes = words.boxed.BoxedChecker(boxes)
    return border, boxes, fontstore, headlines, textnavigators


def load_basic(
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        pagesizes: str,
        headerfooters: str,
        pages=None,
):
    text = serializeraw.load_document(text, pages=pages)
    text_position = serializeraw.load_textpositions(text_position, pages=pages)
    textnavigators = hey.textnavigator.navigator.create_pagetextnavigators(
        text=text,
        text_positions=text_position,
    )

    fontstore = hey.fonts.store.create_fontstore(font_header, font_content)
    sizeandborder = serializeraw.load_pageborders(pagesizes, pages=pages)

    headerfooters = serializeraw.load_headerfooter(
        headerfooters,
        pages=pages,
    )

    return sizeandborder, fontstore, textnavigators, headerfooters


def load_extracted(
        extracted_text,
        headlines,
        pages=None,
) -> typing.Tuple[typing.List, iamraw.Border]:
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    extracted_text = serializeraw.load_text(
        extracted_text,
        headlines,
        pages=pages,
    )
    return extracted_text, headlines
