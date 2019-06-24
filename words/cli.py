#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from utila import featurepack

from words import PROCESS_NAME
from words import ROOT
from words import __version__

DESCRIPTION = 'TODO'

WORKPLAN = []


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
