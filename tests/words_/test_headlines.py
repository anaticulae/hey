# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from hey.textnavigator.navigator import PageTextNavigator
from hey.textnavigator.navigator import create_pagetextnavigator
from tests.groupme_.test_numbers import restructured_sizeandborder
from tests.hey_.test_fonts_store import restructured_fontstore
from tests.sections_ import restructured_document  # pylint:disable=W0611
from tests.sections_ import restructured_horizontals
from tests.sections_ import restructured_text_positions
from tests.sections_.test_sections import restructured
from words.feature.headlines import Headline
from words.feature.headlines import extract_headlines


# def extract_headlines(sections: Sections, text, fontstore: FontStore):
def test_headlines_extract_headlines(
        restructured,
        restructured_text_positions,
        restructured_document,
        restructured_fontstore,
        restructured_sizeandborder,
        restructured_horizontals,
):
    sections = restructured
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


# def extract_headlines(sections: Sections, text, fontstore: FontStore):

# RESTRUCT_FONT_CONTENT = join(RESTRUCT, 'rawmaker__fonts_content.yaml')
# RESTRUCT_FONT_HEADER = join(RESTRUCT, 'rawmaker__fonts_header.yaml')
# RESTRUCT_HORIZONTAL = join(RESTRUCT, 'rawmaker__boxes_horizontal.yaml')
# RESTRUCT_ONELINE_FONT_CONTENT = join(RESTRUCT,
#                                      'rawmaker__oneline_fonts_content.yaml')
# RESTRUCT_ONELINE_FONT_HEADER = join(RESTRUCT,
#                                     'rawmaker__oneline_fonts_header.yaml')
# RESTRUCT_ONELINE_POSITION = join(RESTRUCT,
#                                  'rawmaker__oneline_text_positions.yaml')
# RESTRUCT_ONELINE_TEXT = join(RESTRUCT, 'rawmaker__oneline_text_text.yaml')
# RESTRUCT_PAGESIZE = join(RESTRUCT, 'rawmaker__border_pages.yaml')
# RESTRUCT_TEXT_POSITION = join(RESTRUCT, 'rawmaker__text_positions.yaml')
# RESTRUCT_TEXT = join(RESTRUCT, 'rawmaker__text_text.yaml')
# RESTRUCT_TOC = join(RESTRUCT, 'rawmaker__toc.yaml')
