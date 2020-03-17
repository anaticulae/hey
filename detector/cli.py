# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
from utila import ResultFile as RF
from utila import create_step as step
from utila import featurepack

from detector import PROCESS
from detector import ROOT
from detector import __version__

DESCRIPTION = ''

ResultFile = lambda producer, name: RF(producer=producer, name=name)  # pylint:disable=C0103

TITLEPAGE_STEP = 'titlepage'

TITLEPAGE_OUTPUT = 'detected'

WORKPLAN = [
    step(
        'bibliography',
        inputs=[
            ResultFile('rawmaker', 'text_text'),
            ResultFile('rawmaker', 'text_positions'),
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=(TITLEPAGE_OUTPUT,),
    ),
    step(
        TITLEPAGE_STEP,
        inputs=[
            ResultFile('rawmaker', 'oneline_text_text'),
            ResultFile('rawmaker', 'oneline_text_positions'),
        ],
        output=(TITLEPAGE_OUTPUT,),
    ),
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='detector.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            version=__version__,
        ),
    )
