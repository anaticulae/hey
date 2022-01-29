# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import os

import iamraw
import serializeraw
import utila


def work(
    xfigure: str,
    ximage: str,
    xtable: str,
    xcode: str,
    pages: tuple,
) -> str:
    # load
    figure = load_ifexists(xfigure, pages)
    image = load_ifexists(ximage, pages)
    table = load_ifexists(xtable, pages)
    code = load_ifexists(xcode, pages)
    # merge together
    merged = merge(figure, image, table, code)
    # dump
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
    # remove duplications if table and image/figure detects the same caption
    for page, values in collected.items():
        before = values
        collected[page] = utila.make_unique(values)
        if collected[page] != before:
            before: str = utila.NEWLINE.join(str(item) for item in before)
            utila.error(f'duplicated caption:\n{before}')
    # convert to expected data structure
    result = [
        iamraw.PageContentCaption(page=key, content=values)
        for key, values in collected.items()
    ]
    for page in result:
        # sort content by line number
        page.content.sort(key=lambda x: x.line)
    result.sort(key=lambda x: x.page)
    return result
