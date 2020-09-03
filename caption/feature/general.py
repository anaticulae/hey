# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os

import iamraw
import caption.serialize


def work(figure: str, image: str, table: str, pages: tuple) -> str:
    figure = load_ifexists(figure, pages)
    image = load_ifexists(image, pages)
    table = load_ifexists(table, pages)

    merged = merge(figure, image, table)

    dumped = caption.serialize.dump_captions(merged)
    return dumped


def load_ifexists(path: str, pages: tuple = None):
    if not os.path.exists(path):
        return []
    result = caption.serialize.load_captions(path, pages=pages)
    return result


def merge(*items) -> iamraw.PageContentCaptions:
    collected = collections.defaultdict(list)

    for item in items:
        for page in item:
            collected[page.page].extend(page.content)

    result = [
        iamraw.PageContentCaption(page=key, content=values)
        for key, values in collected.items()
    ]

    for page in result:
        # sort content by line number
        page.content.sort(key=lambda x: x.line)

    result.sort(key=lambda x: x.page)
    return result
