#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from utila import create_step

from sections import PROCESS_NAME
from sections import ROOT
from sections import __version__
from sections.command.patch import featurepack
from sections.feature.chapter import work as work_chapter
from sections.feature.index import work as work_index
from sections.feature.sections import work as work_sections
from sections.feature.title import work as work_title
from sections.feature.toc import work as work_toc
from sections.feature.whitepage import work as work_whitepage

DESCRIPTION = ('The sections tool analyses every single page of an pdf file '
               'and determines the likelihood to be an feature')

WORKPLAN = [
    create_step(
        PROCESS_NAME,
        work_index,
        inputs=[
            ('rawmaker', 'oneline_text_text'),
        ],
        output=('likelihood_index',),
    ),
    create_step(
        PROCESS_NAME,
        work_toc,
        inputs=[
            ('rawmaker', 'oneline_text_text'),
        ],
        output=('likelihood_toc',),
    ),
    create_step(
        PROCESS_NAME,
        work_title,
        inputs=[
            ('rawmaker', 'text_text'),
            ('rawmaker', 'fonts_header'),
            ('rawmaker', 'fonts_content'),
        ],
        output=('likelihood_title',),
    ),
    create_step(
        PROCESS_NAME,
        work_whitepage,
        inputs=[
            ('rawmaker', 'text_text'),
            ('rawmaker', 'text_positions'),
            ('rawmaker', 'boxes_horizontal'),
        ],
        output=('likelihood_whitepage',),
    ),
    create_step(
        PROCESS_NAME,
        work_chapter,
        inputs=[
            ('rawmaker', 'text_text'),
            ('rawmaker', 'text_positions'),
            ('rawmaker', 'toc'),
        ],
        output=('likelihood_chapter',),
    ),
    create_step(
        PROCESS_NAME,
        work_sections,
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
        feature_package='sections.feature',
        name=PROCESS_NAME,
        root=ROOT,
        version=__version__,
        workplan=WORKPLAN,
    )
