# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hey.path


def pagenumbers(path: str, prefix: str = '') -> str:
    return hey.path.pathconnector(
        path,
        'groupme',
        'pagenumbers_pagenumbers',
        prefix,
    )


def headerfooters(path: str, prefix: str = '') -> str:
    return hey.path.pathconnector(
        path,
        'groupme',
        'footer_footerheader',
        prefix,
    )


def toc(path: str, prefix: str = '') -> str:
    return hey.path.pathconnector(
        path,
        'groupme',
        'toc_toc',
        prefix,
    )
