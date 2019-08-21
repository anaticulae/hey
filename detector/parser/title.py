# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore
from hey.textnavigator.fonts import bounds_to_textbounds
from hey.textnavigator.navigator import PageTextNavigator


def parse(textnavigator: PageTextNavigator):
    # dimension = textnavigator.
    for bounds, text in textnavigator:
        bounds_to_textbounds(
            bounds,
            text,
        )


def parse_title(raw, scale: float):
    pass
