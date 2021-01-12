# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import caption

DESCRIPTION = 'TODO'

CAPTION_DATA = [
    utila.ResultFile('rawmaker', 'oneline_text_text'),
    utila.ResultFile('rawmaker', 'oneline_text_positions'),
    utila.ResultFile('rawmaker', 'border_pages'),
    utila.ResultFile('groupme', 'footer_footerheader'),
]

WORKPLAN = [
    utila.create_step(
        name='figure',
        inputs=CAPTION_DATA + [
            utila.Pattern('rawmaker__figures_figures/*', 'yaml'),
        ],
        output=('caption',),
    ),
    utila.create_step(
        name='image',
        inputs=CAPTION_DATA + [
            utila.Pattern('rawmaker__images_images/*', 'yaml'),
        ],
        output=('caption',),
    ),
    utila.create_step(
        name='table',
        inputs=CAPTION_DATA + [
            utila.ResultFile('linero', 'table_table'),
        ],
        output=('caption',),
    ),
    utila.create_step(
        'general',
        inputs=[
            utila.ResultFile(caption.PROCESS, 'figure_caption', optional=True),
            utila.ResultFile(caption.PROCESS, 'image_caption', optional=True),
            utila.ResultFile(caption.PROCESS, 'table_caption', optional=True),
        ],
        output=('general',),
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
