#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from utila import create_step as step
from utila import featurepack

from sections import PROCESS_NAME
from sections import ROOT
from sections import __version__

DESCRIPTION = ('The sections tool analyses every single page of an pdf file '
               'and determines the likelihood to be an feature')

WORKPLAN = [
    step(
        'index',
        inputs=[
            ('rawmaker', 'oneline_text_text'),
        ],
        output=('likelihood_index',),
    ),
    step(
        'toc',
        inputs=[
            ('rawmaker', 'oneline_text_text'),
        ],
        output=('likelihood_toc',),
    ),
    step(
        'title',
        inputs=[
            ('rawmaker', 'text_text'),
            ('rawmaker', 'fonts_header'),
            ('rawmaker', 'fonts_content'),
        ],
        output=('likelihood_title',),
    ),
    step(
        'whitepage',
        inputs=[
            ('rawmaker', 'text_text'),
            ('rawmaker', 'text_positions'),
            ('rawmaker', 'boxes_horizontal'),
        ],
        output=('likelihood_whitepage',),
    ),
    step(
        'chapter',
        inputs=[
            ('rawmaker', 'text_text'),
            ('rawmaker', 'text_positions'),
            ('rawmaker', 'toc'),
        ],
        output=('likelihood_chapter',),
    ),
    step(
        'sections',
        inputs=[
            ('sections', 'likelihood_chapter'),
            ('sections', 'likelihood_index'),
            ('sections', 'likelihood_title'),
            ('sections', 'likelihood_toc'),
            ('sections', 'likelihood_whitepage'),
        ],
        output=('likelihood_sections',),
    ),
]


def main():
    # TODO: Introduce mega --command which activates more than one --todo!
    featurepack(
        description=DESCRIPTION,
        featurepackage='sections.feature',
        name=PROCESS_NAME,
        root=ROOT,
        version=__version__,
        workplan=WORKPLAN,
    )
