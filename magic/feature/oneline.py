# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import magic.feature.content


def work(  # pylint:disable=W0613,R0913
    oneline_text: str,
    oneline_textpositions: str,
    sizeandborders: str,
    footerheader: str,
    lists: str,
    blockquotes: str,
    formula: str,
    captions: str,
    table: str,
    figures: str,
    pages: tuple = None,
) -> str:
    data = locals()
    result = magic.feature.content.work(*data.values())
    return result
