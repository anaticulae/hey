# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import tests.resources
import words
import words.feature

SEVENTYTWO_FIRSTPAGE = os.path.join(
    words.ROOT,
    'tests/words_/fixtures/seventytwo_firstpage.txt',
)


def textrequired(pages=None):
    return words.feature.load_resources_frompath(
        tests.resources.MASTER_72PAGES,
        pages=pages,
    )


def firstpage_sentences():
    assert os.path.exists(SEVENTYTWO_FIRSTPAGE), SEVENTYTWO_FIRSTPAGE

    content = utila.file_read(SEVENTYTWO_FIRSTPAGE)
    splitted = content.split(utila.NEWLINE * 2)

    sentences = [item.replace(utila.NEWLINE, ' ').strip() for item in splitted]
    return sentences


FIRST_PAGE_SENTENCES = []
