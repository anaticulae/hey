# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw

import groupme.feature.abbreviation
import tests.resources


def test_groupme_abbreviation_work():
    source = tests.resources.BACHELOR37

    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)

    oneline_text = iamraw.path.text(source, prefix='oneline')
    oneline_textposition = iamraw.path.textposition(source, prefix='oneline')

    dumped = groupme.feature.abbreviation.work(
        text,
        textposition,
        oneline_text,
        oneline_textposition,
        pages=(1,),
    )

    loaded = serializeraw.load_abbreviation_table(dumped)
    assert len(loaded) == 26
