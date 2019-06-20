#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from serializeraw import load_document
from utila import create_step
from utila import featurepack

from groupme import ROOT
from groupme import __version__
from groupme.feature.chapter import work as extract_chapter
from groupme.feature.numbers import work as extract_pagenumbers
from groupme.feature.toc import work as extract_toc

PROCESS_NAME = 'groupme'
DESCRIPTION = 'TODO'
WORKPLAN = [
    create_step(
        PROCESS_NAME,
        extract_chapter,
        inputs=[
            ('rawmaker', 'text_text'),
        ],
        output=('chapter',),
    ),
    create_step(
        PROCESS_NAME,
        extract_toc,
        inputs=[
            ('rawmaker', 'text_text'),
        ],
        output=('toc',),
    ),
    create_step(
        PROCESS_NAME,
        extract_pagenumbers,
        inputs=[
            ('rawmaker', 'text_text'),
            ('rawmaker', 'text_positions'),
        ],
        output=('pagenumbers',),
    )
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        feature_package='groupme.feature',
        name=PROCESS_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
