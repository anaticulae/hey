# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex

import detector.bibliography.alternate
import detector.bibliography.column
import detector.bibliography.data


def extracts(
        text: texmex.PageTextNavigators,
        text_oneline: texmex.PageTextNavigators,
) -> iamraw.BibliographyReferences:
    column = detector.bibliography.column.extracts(text)
    alternate = detector.bibliography.alternate.extracts(text_oneline)

    if (len(alternate) / 2) > len(column):
        # alternate extracts a lot of more possible bibs, therefore we
        # have to punish the number of results. HolyValue: 0.5
        return alternate
    return column
