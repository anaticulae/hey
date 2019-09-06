# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import ResultFile as RF
from utila import create_step as step
from utila import featurepack

from detector import PROCESS_NAME
from detector import ROOT
from detector import __version__

DESCRIPTION = ''

ResultFile = lambda producer, name: RF(producer=producer, name=name)  # pylint:disable=C0103

WORKPLAN = [
    step(
        'title',
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=('page_detected',),
    ),
]


def main():
    featurepack(
        description=DESCRIPTION,
        featurepackage='detector.feature',
        multiprocessed=True,
        name=PROCESS_NAME,
        pages=True,
        root=ROOT,
        singleinput=False,  # require result folder, ignore single pdf file
        version=__version__,
        workplan=WORKPLAN,
    )
