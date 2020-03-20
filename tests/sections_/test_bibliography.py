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


def test_section_bibliography_work():
    source = tests.resources.MASTER72
    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    expected = (
        (60, 0.0),
        (61, 0.0),
        (62, 0.0),
        (63, 0.0),
        (64, 0.0),
        (65, 0.5),
        (66, 0.5),
        (67, 0.5),
        (68, 0.5),
        (69, 0.5),
        (70, 0.5),
        (71, 0.0),
    )
    pages = [page for page, _ in expected]
    extracted = sections.feature.bibliography.work(
        text,
        textposition,
        pages=pages,
    )
    assert len(extracted) > 50, str(extracted)
    loaded = serializeraw.load_likelihood(extracted)

    for page, value in expected:
        selected = utila.select_page(loaded, page=page)
        current = selected.content.value
        assert current >= value, str(selected)
