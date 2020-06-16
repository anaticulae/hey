# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import magic

WORKPLAN = [
    utila.create_step(
        'content',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='text_text'),
        ],
        output=('content',),
    ),
    utila.create_step(
        'complete',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='text_text'),
        ],
        output=('complete',),
    ),
]

DESCRIPTION = """\
Determine type of line (content, list, boxed content, etc.)
"""


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=magic.ROOT,
        featurepackage='magic.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=magic.PROCESS,
            pages=True,
            version=magic.__version__,
        ),
    )
