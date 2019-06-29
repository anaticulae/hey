# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from hey.textnavigator.navigator import create_pagetextnavigator
# pylint:disable=W0611
from tests.fixtures.restruct import restructured
from tests.fixtures.restruct import restructured_document
from tests.fixtures.restruct import restructured_fontstore
from tests.fixtures.restruct import restructured_horizontals
from tests.fixtures.restruct import restructured_sections
from tests.fixtures.restruct import restructured_sizeandborder
from tests.fixtures.restruct import restructured_text_positions
from words.feature.headlines import Headline
from words.feature.headlines import extract_headlines


# def extract_headlines(sections: Sections, text, fontstore: FontStore):
def test_headlines_extract_headlines(
        # pylint:disable=W0621
        restructured_sections,
        restructured_text_positions,
        restructured_document,
        restructured_fontstore,
        restructured_sizeandborder,
        restructured_horizontals,
):
    sections = restructured_sections
    position = restructured_text_positions
    document = restructured_document
    sizeandborder = restructured_sizeandborder

    navigator = create_pagetextnavigator(position, document)

    extracted = extract_headlines(
        sections=sections,
        pagetextnavigator=navigator,
        fontstore=restructured_fontstore,
        sizeandborder=sizeandborder,
        horizontals=restructured_horizontals,
        chapter=[0, 1],
    )

    expected = [
        [
            Headline(text='CHAPTER 1', level=1, rawlevel='1'),
            Headline(text='RestructuredText Tutorial', level=2, rawlevel=''),
        ],
        [
            Headline(text='CHAPTER 2', level=1, rawlevel='2'),
            Headline(text='RestructuredText Guide', level=2, rawlevel=''),
            Headline(text='Basics', level=3, rawlevel=''),
            Headline(text='Blockquotes', level=3, rawlevel=''),
            Headline(text='Code: Block', level=3, rawlevel=''),
        ],
    ]

    assert extracted == expected
