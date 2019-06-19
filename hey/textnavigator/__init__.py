# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import List

from iamraw import BoundingBox


def navigator_to_bounds(navigator: 'PageTextNavigator') -> List[BoundingBox]:
    """Extract list of `BoundingBox` from `PageTextNavigator`"""
    return [item for item, _ in navigator]
