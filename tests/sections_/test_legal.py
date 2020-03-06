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

import sections.feature.legal
import tests.resources


def test_legal_work_master116():
    source = tests.resources.MASTER116

    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)
    pages = (0, 1, 2, 3, 4, 5, 96)

    dumped = sections.feature.legal.work(text, textposition, pages=pages)
    assert dumped, dumped

    loaded = serializeraw.load_likelihood(dumped)
    legal_page = utila.select_page(loaded, page=1)
    assert legal_page.content.value == 1.0, str(dumped)
