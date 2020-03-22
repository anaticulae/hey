# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import serializeraw
import texmex


def load(
        text: str,
        textpositions: str,
        headerfooter: str,
        sizeandborder: str,
        pages: tuple = None,
) -> texmex.PageTextContentNavigators:
    text = serializeraw.load_document(text, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)
    navigators = texmex.create_pagetextnavigators(
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
    navigators = texmex.create_pagetextcontentnavigators(
        navigators=navigators,
        headerfooter=headerfooter,
        sizeandborder=sizeandborder,
        validate_leftright=False,
        pages=pages,
    )
    return navigators


def load_frompath(path: str, pages: tuple = None):
    text = iamraw.path.text(path, prefix='oneline')
    textpositions = iamraw.path.textposition(path, prefix='oneline')
    sizeandborder = iamraw.path.sizeandborder(path)
    headerfooter = iamraw.path.headerfooters(path)
    loaded = load(
        text,
        textpositions,
        headerfooter,
        sizeandborder,
        pages=pages,
    )
    return loaded
