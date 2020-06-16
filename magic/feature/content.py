# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import magic.data


def work(
        text: str,
        textpositions: str,
        sizeandborders: str,
        footerheader: str,
        lists: str,
        pages: tuple = None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborders,
        footerheader,
        pages=pages,
    )
    lists = serializeraw.load_lists(lists, pages=pages)

    result = []
    for navigator in ptcns:
        listinstance = utila.select_page(lists, navigator.page)
        analyzed = analyze_page(navigator, listinstance)
        result.append(analyzed)

    dumped = magic.data.dump_types(result)
    return dumped


def analyze_page(ptcn, lists):
    result = []
    for index, line in enumerate(ptcn):  # pylint:disable=W0612
        if islist(index, lists):
            result.append((index, magic.data.ContentType.LIST))
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
