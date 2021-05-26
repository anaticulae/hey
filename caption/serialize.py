# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import iamraw
import serializeraw
import utila


def load_image_informations_fromfiles(
    files: str,
    pages: tuple = None,
) -> iamraw.PageContentImageInfos:
    # TODO: MOVE TO IAMRAW
    collected = collections.defaultdict(list)
    for source in files:
        loaded = serializeraw.load_image_info(source)
        if utila.should_skip(loaded.page, pages):
            continue
        collected[loaded.page].append(loaded)
    result = [
        iamraw.PageContentImageInfo(page=key, content=value)
        for key, value in collected.items()
    ]
    result.sort(key=lambda x: x.page)
    return result
