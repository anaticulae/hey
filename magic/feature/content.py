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
import serializeraw
import serializeraw.images
import utila


def work(  # pylint:disable=R0913,R0914,
        text: str,
        textpositions: str,
        sizeandborders: str,
        footerheader: str,
        lists: str,
        blockquotes: str,
        formula: str,
        captions: str,
        table: str,
        figures: str,
        pages: tuple = None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborders,
        footerheader,
        pages=pages,
    )
    lists = expand_lists(load_content(serializeraw.load_lists, lists, pages))
    blockquotes = load_content(serializeraw.load_blockquotes, blockquotes, pages) # yapf:disable
    formula = load_content(serializeraw.load_formulas, formula, pages)
    captions = load_content(serializeraw.load_captions, captions, pages)
    tables = load_content(serializeraw.load_tables, table, pages)
    # TODO: THINK ABOUT DUPLICATED PAGES?
    figures = utila.flatten([
        load_content(
            serializeraw.images.load_image_informations_frompath,
            item,
            pages,
        ) for item in figures
    ])

    result = []
    for navigator in ptcns:
        listinstance = utila.select_page(lists, navigator.page)
        blockquoteinstance = utila.select_page(blockquotes, navigator.page)
        formulainstance = utila.select_page(formula, navigator.page)
        captioninstance = utila.select_page(captions, navigator.page)
        tableinstance = utila.select_page(tables, navigator.page)
        figureinstance = utila.select_page(figures, navigator.page)

        analyzed = analyze_page(
            navigator,
            listinstance,
            blockquoteinstance,
            formulainstance,
            captioninstance,
            tableinstance,
            figureinstance,
        )
        result.append(analyzed)

    dumped = serializeraw.dump_types(result)
    return dumped


def load_content(loader, content, pages):
    if not os.path.exists(content):
        # inform integrator about missing resource
        utila.error(f'missing: {content}')
        return []
    content = loader(content, pages=pages)
    return content


def analyze_page(ptcn, lists, blockquotes, formula, captions, tables, figures):
    # How to determine order of checking cause more than result is
    # possible?

    # Run figure and table before caption, cause caption can badly include
    # some text which is part of the figure and should not be judged as
    # caption or text.
    result = []
    for index, line in enumerate(ptcn):  # pylint:disable=W0612
        if islist(index, lists):
            result.append((index, iamraw.PageContentType.LIST))
            continue
        if isblockquote(index, blockquotes):
            result.append((index, iamraw.PageContentType.BLOCKQUOTE))
            continue
        if isformula(index, formula):
            result.append((index, iamraw.PageContentType.FORMULA))
            continue
        if isfigure(line, figures):
            result.append((index, iamraw.PageContentType.FIGURE))
            continue
        if istable(line, tables):
            result.append((index, iamraw.PageContentType.TABLE))
            continue
        if iscaption(index, captions):
            result.append((index, iamraw.PageContentType.CAPTION))
            continue
    return iamraw.PageContentContentType(page=ptcn.page, content=result)


def islist(line: int, listinstances: set) -> bool:
    if not listinstances:
        return False
    return line in listinstances


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


def iscaption(line, captions):
    if not captions:
        return False
    if not captions.content:
        return False
    captions = captions.content
    lines = expand_multiline(captions)
    if line in lines:
        return True
    return False


def istable(line, tables):
    if not tables:
        return False
    if not tables.content:
        return False
    for table in tables.content:
        if utila.rectangle_inside(table.bounding, line.bounding, diff=5.0):
            return True
    return False


def isfigure(line, figures):
    if not figures:
        return False
    if not figures.content:
        return False
    for figure in figures.content:
        if utila.rectangle_inside(figure.bounding, line.bounding):
            return True
    return False


def expand_multiline(captions: iamraw.Captions) -> set:
    lines = [
        utila.ranged_tuple(item.line, item.lineend + 1) for item in captions
    ]
    lines = [item for item in lines if item]
    lines = utila.flatten(lines)
    # make unique
    lines = set(lines)  # pylint:disable=R0204
    return lines


def expand_lists(lists):
    """Determine lines which are covered by lines. Expand lists which
    are expanded over more than one page."""
    result = collections.defaultdict(set)
    for page in lists:
        for listi in page.content:
            areas = listi.area
            areas = areas if isinstance(areas[0], tuple) else [areas]
            for index, area in enumerate(areas, start=page.page):
                result[index].update(area)
    result = {page: content for page, content in result.items()}
    return result
