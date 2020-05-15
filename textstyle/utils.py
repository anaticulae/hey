# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import textstyle


def flatten(pages: textstyle.PageTextPropertiesList) -> textstyle.TextProperties: # yapf:disable
    result = []
    for page in pages:
        for length, size, font, distance, ypos in zip(
                page.length,
                page.sizes,
                page.fonts,
                page.distances,
                page.ypos,
        ):
            result.append(
                textstyle.TextProperty(
                    length=length,
                    size=size,
                    font=font,
                    before=distance.top,
                    after=distance.bottom,
                    top=ypos[0],
                    bottom=ypos[1],
                ))
    return result
