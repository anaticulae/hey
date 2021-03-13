# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import magic

DESCRIPTION = """\
Determine type of line (content, list, boxed content, etc.)
"""

# yapf:disable
WORKPLAN = [
    utila.create_step(
        'content',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('words', 'list_list', optional=True),
            utila.ResultFile('textflow', 'blockquote_blockquote', optional=True),
            utila.ResultFile('detector', 'formula_formula', optional=True),
            utila.ResultFile('caption', 'general_general', optional=True),
            utila.ResultFile('linero', 'table_table', optional=True),
            utila.Directory('rawmaker__figures_figures', optional=True),
        ],
        output=('content_normal', 'content'),
    ),
]
# yapf:enable


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
