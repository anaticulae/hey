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

import groupme.abbreviation
import groupme.abbreviation.parser


def work(
        text: str,
        textposition: str,
        text_oneline: str,
        textposition_oneline: str,
        pages: tuple = None,
) -> str:
    text_oneline = serializeraw.load_document(text_oneline, pages=pages)
    textposition_oneline = serializeraw.load_textpositions(
        textposition_oneline,
        pages=pages,
    )

    text = serializeraw.load_document(text, pages=pages)
    textposition = serializeraw.load_textpositions(textposition, pages=pages)

    oneline = texmex.create_pagetextnavigators(
        text_oneline,
        textposition_oneline,
    )

    normal = texmex.create_pagetextnavigators(
        text,
        textposition,
    )

    data = groupme.abbreviation.AbbreviationData(normal=normal, oneline=oneline)

    parsed = groupme.abbreviation.parser.parse(data)

    dumped = serializeraw.dump_abbreviation_table(parsed)
    return dumped
