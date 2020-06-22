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


def work(  # pylint:disable=R0914
        text: str,
        textpositions: str,
        sizeandborders: str,
        footerheader: str,
        lists: str,
        blockquotes: str,
        formula: str,
        pages: tuple = None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborders,
        footerheader,
        pages=pages,
    )
    lists = load_content(serializeraw.load_lists, lists, pages)
    blockquotes = load_content(serializeraw.load_blockquotes, blockquotes, pages) # yapf:disable
    formula = load_content(serializeraw.load_formulas, formula, pages)

    result = []
    for navigator in ptcns:
        listinstance = utila.select_page(lists, navigator.page)
        blockquoteinstance = utila.select_page(blockquotes, navigator.page)
        formulainstance = utila.select_page(formula, navigator.page)

        analyzed = analyze_page(
            navigator,
            listinstance,
            blockquoteinstance,
            formulainstance,
        )
        result.append(analyzed)

    dumped = magic.data.dump_types(result)
    return dumped


def load_content(loader, content, pages):
    if not os.path.exists(content):
        return []
    content = loader(content, pages=pages)
    return content


def analyze_page(ptcn, lists, blockquotes, formula):
    result = []
    for index, line in enumerate(ptcn):  # pylint:disable=W0612
        if islist(index, lists):
            result.append((index, magic.data.ContentType.LIST))
            continue
        if isblockquote(index, blockquotes):
            result.append((index, magic.data.ContentType.BLOCKQUOTE))
            continue
        if isformula(index, formula):
            result.append((index, magic.data.ContentType.FORMULA))
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


def isblockquote(line, quotes):
    if not quotes:
        return False
    if not quotes.content:
        return False
    quotes = quotes.content
    for area, _ in quotes:
        if line in area:
            return True
    return False


def isformula(line, formulas):
    if not formulas:
        return False
    if not formulas.content:
        return False
    formulas = formulas.content
    lines = [item.line for item in formulas]
    if line in lines:
        return True
    return False
