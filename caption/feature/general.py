# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import caption.data
import caption.serialize


def work(image: str, pages: tuple) -> str:
    image = caption.serialize.load_captions(image, pages=pages)

    merged = merge(image)

    dumped = caption.serialize.dump_captions(merged)
    return dumped


def merge(*items) -> caption.data.PageContentCaptions:
    collected = collections.defaultdict(list)

    for item in items:
        for page in item:
            collected[page.page].extend(page.content)

    result = [
        caption.data.PageContentCaption(page=key, content=values)
        for key, values in collected.items()
    ]

    for page in result:
        # sort content by line number
        page.content.sort(key=lambda x: x.line)

    result.sort(key=lambda x: x.page)
    return result
