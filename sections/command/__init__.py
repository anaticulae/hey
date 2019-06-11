#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from os.path import join

from hey.utils import featurepack
from sections import PROCESS_NAME
from sections import ROOT
from sections import __version__

DESCRIPTION = 'TODO'
WORKPLAN = [
    # create_step(
    #     PROCESS_NAME,
    #     extract_chapter,
    #     inputs=[
    #         ('rawmaker', 'text_text'),
    #     ],
    #     output=('chapter',),
    # ),
]


def main():
    featurepack(
        description=DESCRIPTION,
        feature_package='sections.feature',
        name=PROCESS_NAME,
        root=ROOT,
        version=__version__,
        workplan=WORKPLAN,
    )
