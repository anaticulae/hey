# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# TODO: IMPROVE NAMING

import dataclasses
import typing

import iamraw
import serializeraw

import hey.fonts.store
import hey.textnavigator.navigator


@dataclasses.dataclass
class BasicRequiredResources:
    sizeandborder: iamraw.PageSizeBorderList
    fontstore: hey.fonts.store.FontStore
    textnavigators: hey.textnavigator.navigator.PageTextNavigators
    # TODO: fix iamraw
    headerfooters: typing.List[iamraw.PageContentFooterHeader]


def load_basic(
        text: str,
        text_position: str,
        font_header: str,
        font_content: str,
        pagesizes: str,
        headerfooters: str,
        pages=None,
) -> BasicRequiredResources:
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

    result = BasicRequiredResources(
        sizeandborder=sizeandborder,
        fontstore=fontstore,
        textnavigators=textnavigators,
        headerfooters=headerfooters,
    )
    return result
