# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import texmex

import detector.bibliography.data
import detector.bibliography.strategy


def work(
        text: str,
        textpositions: str,
        oneline_text: str,
        oneline_textpositions: str,
        pages: tuple = None,
) -> str:
    text = serializeraw.load_document(text, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)

    oneline_text = serializeraw.load_document(oneline_text, pages=pages)
    oneline_textpositions = serializeraw.load_textpositions(
        oneline_textpositions,
        pages=pages,
    )

    textnavigators = texmex.create_pagetextnavigators(
        text,
        textpositions,
    )
    onelines = texmex.create_pagetextnavigators(
        oneline_text,
        oneline_textpositions,
    )

    extracted = detector.bibliography.strategy.extracts(
        textnavigators,
        onelines,
    )

    dumped = serializeraw.dump_bibliography_reference(extracted)
    return dumped
