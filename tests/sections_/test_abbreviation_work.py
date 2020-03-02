# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import serializeraw
import utila

import sections.feature.abbreviation
import tests.resources


def test_sections_abbreviations_work():
    source = tests.resources.BACHELOR37
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    pages = (0, 1, 2, 5, 6)
    extracted = sections.feature.abbreviation.work(
        text,
        textposition,
        pages=pages,
    )
    assert len(extracted) > 50, str(extracted)
    loaded = serializeraw.load_likelihood(extracted)
    selected = utila.select_page(loaded, page=1)
    assert selected.content.value >= 0.8, str(selected)
