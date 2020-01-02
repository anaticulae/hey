# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import hey.path
import hey.textnavigator.navigator as htn


def load(
        text: str,
        textpositions: str,
        headerfooter: str,
        sizeandborder: str,
        pages: tuple = None,
) -> htn.PageTextContentNavigators:
    text = serializeraw.load_document(text, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)
    navigators = htn.create_pagetextnavigators(
        text,
        textpositions,
    )

    headerfooter = serializeraw.load_headerfooter(
        headerfooter,
        pages=pages,
    )

    sizeandborder = serializeraw.load_pageborders(
        sizeandborder,
        pages=pages,
    )

    navigators = htn.create_pagetextcontentnavigators(
        navigators=navigators,
        headerfooter=headerfooter,
        sizeandborder=sizeandborder,
        validate_leftright=False,
        pages=pages,
    )
    return navigators


def load_frompath(path: str, pages: tuple = None):
    text = hey.path.text(path, prefix='oneline')
    textpositions = hey.path.textposition(path, prefix='oneline')
    sizeandborder = hey.path.sizeandborder(path)
    headerfooter = hey.path.headerfooters(path)
    loaded = load(
        text,
        textpositions,
        headerfooter,
        sizeandborder,
        pages=pages,
    )
    return loaded
