# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import caption

RF = utila.ResultFile

DESCRIPTION = 'TODO'

WORKPLAN = [
    utila.create_step(
        'image',
        inputs=[
            RF(producer='rawmaker', name='text_text'),
            RF(producer='rawmaker', name='text_positions'),
            RF(producer='rawmaker', name='oneline_text_text'),
            RF(producer='rawmaker', name='oneline_text_positions'),
        ],
        output=('caption',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=caption.ROOT,
        featurepackage='caption.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=caption.PROCESS,
            pages=True,
            version=caption.__version__,
        ),
    )
