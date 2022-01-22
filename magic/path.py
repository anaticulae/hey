# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def content(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'magic', 'content_content', prefix)


def content_oneline(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'magic', 'oneline_content', prefix)
