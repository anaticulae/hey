# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import typing

import iamraw
import serializeraw

import hey.fonts.store
import hey.textnavigator.navigator
import words.boxed
import words.headlines


@dataclasses.dataclass
class TextRequiredResources:
    border: iamraw.Border
    boxes: words.boxed.BoxedChecker
    fontstore: hey.fonts.store.FontStore
    headlines: iamraw.PagesHeadlineList
    textnavigators: hey.textnavigator.navigator.PageTextNavigators


def load_resources(
        text: str,
        textposition: str,
        fontheader: str,
        fontcontent: str,
        headlines: str,
        pagesizes: str,
        boxes: str,
        headerfooters: str,
        pages=None,
) -> TextRequiredResources:
    """Load content from path and create required object"""
    text = serializeraw.load_document(text, pages=pages)
    position = serializeraw.load_textpositions(textposition, pages=pages)
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    boxes = serializeraw.load_boxes(boxes, pages=pages)

    fontstore = hey.fonts.store.create_fontstore(fontheader, fontcontent)

    textnavigators = hey.textnavigator.navigator.create_pagetextnavigators(
        text=text,
        text_positions=position,
    )
    contentborder = serializeraw.load_pageborders(pagesizes, pages=pages)

    headerfooters = serializeraw.load_headerfooter(
        headerfooters,
        pages=pages,
    )

    border = words.headlines.contentborder(
        contentborder,
        headerfooters,
    )

    boxed = words.boxed.BoxedChecker(boxes)

    result = TextRequiredResources(
        border=border,
        boxes=boxed,
        fontstore=fontstore,
        headlines=headlines,
        textnavigators=textnavigators,
    )
    return result


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
