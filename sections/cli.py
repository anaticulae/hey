#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
from utila import ResultFile as RF
from utila import create_step as step
from utila import featurepack

from sections import PROCESS
from sections import ROOT
from sections import __version__

DESCRIPTION = ('The sections tool analyses every single page of an pdf file '
               'and determines the likelihood to be an feature')

ResultFile = lambda producer, name: RF(producer=producer, name=name)

WORKPLAN = [
    step(
        'index',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
        ],
        output=('likelihood',),
    ),
    step(
        'toc',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
        ],
        output=('likelihood',),
    ),
    step(
        'title',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'fonts_header'),
            ResultFile('rawmaker', 'fonts_content'),
        ],
        output=('likelihood',),
    ),
    step(
        'whitepage',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('likelihood',),
    ),
    step(
        'chapter',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('rawmaker', 'toc_toc'),
        ],
        output=('likelihood',),
    ),
    step(
        'section',
        inputs=[
            ResultFile('sections', 'chapter_likelihood'),
            ResultFile('sections', 'index_likelihood'),
            ResultFile('sections', 'title_likelihood'),
            ResultFile('sections', 'toc_likelihood'),
            ResultFile('sections', 'whitepage_likelihood'),
        ],
        output=('result',),
    ),
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='sections.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            version=__version__,
        ),
    )
