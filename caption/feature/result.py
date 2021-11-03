# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os

import iamraw
import serializeraw


def work(figure: str, image: str, table: str, code: str, pages: tuple) -> str:
    figure = load_ifexists(figure, pages)
    image = load_ifexists(image, pages)
    table = load_ifexists(table, pages)
    code = load_ifexists(code, pages)

    merged = merge(figure, image, table, code)

    dumped = serializeraw.dump_captions(merged)
    return dumped


def load_ifexists(path: str, pages: tuple = None):
    if not os.path.exists(path):
        return []
    result = serializeraw.load_captions(path, pages=pages)
    return result


def merge(*items) -> iamraw.PageContentCaptions:
    collected = collections.defaultdict(list)
    # merge pages together
    for item in items:
        for page in item:
            collected[page.page].extend(page.content)
    # convert to expected data structure
    result = [
        iamraw.PageContentCaption(page=key, content=values)
        for key, values in collected.items()
    ]
    # TODO: REMOVE DUPLICATION?
    for page in result:
        # sort content by line number
        page.content.sort(key=lambda x: x.line)
    result.sort(key=lambda x: x.page)
    return result
