# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import magic

DESCRIPTION = """\
Determine type of line (content, list, boxed content, etc.)
"""

RESOURCES = [
    utilo.ResultFile('rawmaker', 'border_pages'),
    utilo.ResultFile('groupme', 'footer_footerheader'),
    utilo.ResultFile('words', 'list_list', optional=True),
    utilo.ResultFile('textflow', 'blockquote_blockquote', optional=True),
    utilo.ResultFile('detector', 'formula_formula', optional=True),
    utilo.ResultFile('caption', 'result_result', optional=True),
    utilo.ResultFile('tablero', 'decide_decide', optional=True),
    utilo.Directory('rawmaker__images_images', optional=True),
]

WORKPLAN = [
    utilo.create_step(
        'content',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
        ] + RESOURCES,
        output=('content',),
    ),
    utilo.create_step(
        'oneline',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
        ] + RESOURCES,
        output=('content',),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=magic.ROOT,
        featurepackage='magic.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=magic.PROCESS,
            pages=True,
            version=magic.__version__,
        ),
    )
