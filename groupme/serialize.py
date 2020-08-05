# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import yaml


def load_leftright_border(path: str, pages: tuple = None) -> dict:
    # TODO: MOVE TO SERIALIZERAW
    raw = utila.from_raw_or_path(
        path,
        ftype='yaml',
        fname='groupme__border_leftright',
    )
    loaded = yaml.safe_load(raw)
    lookup = {}
    for line in loaded:
        page, border = line.split(maxsplit=1)
        page = int(page)
        border = utila.parse_tuple(border, length=4)
        if utila.should_skip(page, pages):
            continue
        # content = utila.parse_tuple(border)
        lookup[page] = border
    return lookup
