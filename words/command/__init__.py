#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from os.path import join

from utila import create_step

import words
from sections.command.patch import featurepack

DESCRIPTION = 'TODO'

WORKPLAN = []


def main():
    # TODO: Introduce mega --command which activates more than one --todo!
    featurepack(
        description=DESCRIPTION,
        feature_package='words.feature',
        name=words.PROCESS_NAME,
        root=words.ROOT,
        version=words.__version__,
        workplan=WORKPLAN,
    )
