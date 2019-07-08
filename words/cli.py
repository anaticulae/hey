#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from utila import ResultFile as RF
from utila import create_step as step
from utila import featurepack

from words import PROCESS_NAME
from words import ROOT
from words import __version__

DESCRIPTION = 'TODO'

ResultFile = lambda producer, name: RF(producer=producer, name=name)

WORKPLAN = [
    step(
        'headlines',
        inputs=[
            ResultFile('sections', 'sections_result'),
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('rawmaker', 'fonts_header'),
            ResultFile('rawmaker', 'fonts_content'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('rawmaker', 'boxes_horizontal'),
        ],
        output=('headlines',),
    ),
    step(
        'text',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('rawmaker', 'fonts_header'),
            ResultFile('rawmaker', 'fonts_content'),
            ResultFile('words', 'headlines_headlines'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('rawmaker', 'boxes_horizontal'),
            ResultFile('rawmaker', 'boxes_boxes'),
        ],
        output=('text',),
    ),
    step(
        'list',
        inputs=[
            ResultFile('words', 'text_text'),
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('words', 'headlines_headlines'),
            ResultFile('rawmaker', 'border_pages'),
            ResultFile('rawmaker', 'boxes_horizontal'),
        ],
        output=('list',),
    )
]


def main():
    # TODO: Introduce mega --command which activates more than one --todo!
    featurepack(
        description=DESCRIPTION,
        featurepackage='words.feature',
        name=PROCESS_NAME,
        root=ROOT,
        version=__version__,
        workplan=WORKPLAN,
    )
