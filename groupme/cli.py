#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
from utila import ResultFile
from utila import create_step as step
from utila import featurepack

from groupme import PROCESS
from groupme import ROOT
from groupme import __version__

DESCRIPTION = 'TODO'

TOC_STEP = 'toc'
TOC_OUTPUT = 'toc'

WORKPLAN = [
    step(
        'abbreviation',
        inputs=[
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
            ResultFile(producer='rawmaker', name='oneline_text_text'),
            ResultFile(producer='rawmaker', name='oneline_text_positions'),
        ],
        output=('abbreviation',),
    ),
    step(
        'area',
        inputs=[
            ResultFile(producer='rawmaker', name='boxes_boxes'),
            ResultFile(producer='linero', name='table_table'),
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('area',),
    ),
    step(
        'border',
        inputs=[
            ResultFile(producer='rawmaker', name='border_pages'),
            ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('leftright',),
    ),
    step(
        'distance',
        inputs=[
            ResultFile(producer='groupme', name='area_area'),
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('distance',),
    ),
    step(
        TOC_STEP,
        inputs=[
            ResultFile(producer='rawmaker', name='oneline_text_text'),
            ResultFile(producer='rawmaker', name='oneline_text_positions'),
            ResultFile(producer='groupme', name='footer_footerheader'),
            ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=(TOC_OUTPUT,),
    ),
    step(
        'figuretable',
        inputs=[
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
            ResultFile(producer='rawmaker', name='oneline_text_text'),
            ResultFile(producer='rawmaker', name='oneline_text_positions'),
            ResultFile(producer='groupme', name='footer_footerheader'),
            ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('figuretable',),
    ),
    step(
        'tabletable',
        inputs=[
            ResultFile(producer='rawmaker', name='oneline_text_text'),
            ResultFile(producer='rawmaker', name='oneline_text_positions'),
            ResultFile(producer='groupme', name='footer_footerheader'),
            ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('tabletable',),
    ),
    step(
        'pagenumbers',
        inputs=[
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('pagenumbers',),
    ),
    step(
        'footer',
        inputs=[
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
            ResultFile(producer='rawmaker', name='fonts_header'),
            ResultFile(producer='rawmaker', name='fonts_content'),
            ResultFile(producer='rawmaker', name='horizontals_horizontals'),
            ResultFile(producer='rawmaker', name='border_pages'),
            ResultFile(producer='groupme', name='pagenumbers_pagenumbers'),
        ],
        output=('footerheader',),
    )
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='groupme.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=PROCESS,
            pages=True,
            version=__version__,
        ),
    )
