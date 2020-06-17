# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import serializeraw
import utila

import magic.data


def work(
        text: str,
        textpositions: str,
        sizeandborders: str,
        footerheader: str,
        lists: str,
        blockquotes: str,
        pages: tuple = None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborders,
        footerheader,
        pages=pages,
    )
    if os.path.exists(lists):
        lists = serializeraw.load_lists(lists, pages=pages)
    else:
        lists = []
    if os.path.exists(blockquotes):
        # optional blockquotes parameter
        blockquotes = serializeraw.load_blockquotes(blockquotes, pages=pages)
    else:
        blockquotes = []

    result = []
    for navigator in ptcns:
        listinstance = utila.select_page(lists, navigator.page)
        blockquoteinstance = utila.select_page(blockquotes, navigator.page)

        analyzed = analyze_page(
            navigator,
            listinstance,
            blockquoteinstance,
        )
        result.append(analyzed)

    dumped = magic.data.dump_types(result)
    return dumped


def analyze_page(ptcn, lists, blockquotes):
    result = []
    for index, line in enumerate(ptcn):  # pylint:disable=W0612
        if islist(index, lists):
            result.append((index, magic.data.ContentType.LIST))
            continue
        if isblockquote(index, blockquotes):
            result.append((index, magic.data.ContentType.BLOCKQUOTE))
            continue
    return magic.data.PageContentContentType(page=ptcn.page, content=result)


def islist(line, listinstances):
    if not listinstances:
        return False
    if not listinstances.content:
        return False
    listinstances = listinstances.content
    for instance_ in listinstances:
        if line in instance_.area:
            return True
    return False


def isblockquote(line, quotes):  # pylint:disable=W0613
    if not quotes:
        return False
    return False
