# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Requirements:
    We do not check the header, because it is required, that this header
    is fixed.

Example:
    master/page_72_noimages_toc.pdf

TODO: Think about header
"""
import groupme.footer


class MovingFooterStrategy(groupme.footer.FooterHeaderDetectionStrategy):
    pass
