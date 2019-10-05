# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This strategy aims to detect footer which contains only a page number
and distance to text before.

Example:
    docu/howto_argparse.pdf
    technical/page_24_color_figures_images.pdf

"""
import groupme.footer


class PageNumberStrategy(groupme.footer.FooterHeaderDetectionStrategy):
    pass
