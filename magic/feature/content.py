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
import serializeraw.images
import utilo


def work(  # pylint:disable=R0913
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
    ptcns = serializeraw.ptcn_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborder=sizeandborders,
        headerfooter=footerheader,
        pages=pages,
    )
    lists = expand_lists(load_content(serializeraw.load_lists, lists, pages))
    blockquotes = load_content(serializeraw.load_blockquotes, blockquotes, pages) # yapf:disable
    formula = load_content(serializeraw.load_formulas, formula, pages)
    captions = load_content(serializeraw.load_captions, captions, pages)
    tables = load_content(serializeraw.load_tables, table, pages)
    # TODO: THINK ABOUT DUPLICATED PAGES?
    figures = utilo.flat([
        load_content(
            serializeraw.images.load_image_informations_frompath,
            item,
            pages,
        ) for item in figures
    ])
    data = [lists, blockquotes, formula, captions, tables, figures]
    types = determine_types(ptcns, *data)
    return types


def determine_types(  # pylint:disable=R0914
    ptcns,
    lists,
    blockquotes,
    formula,
    captions,
    tables,
    figures,
) -> str:
    result = []
    for navigator in ptcns:
        listinstance = utilo.select_page(lists, navigator.page)
        blockquoteinstance = utilo.select_page(blockquotes, navigator.page)
        formulainstance = utilo.select_page(formula, navigator.page)
        captioninstance = utilo.select_page(captions, navigator.page)
        tableinstance = utilo.select_page(tables, navigator.page)
        figureinstance = utilo.select_page(figures, navigator.page)

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
        utilo.error(f'missing: {content}')
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
        if istable(line, tables):
            result.append((index, iamraw.PageContentType.TABLE))
            continue
        if isfigure(line, figures):
            result.append((index, iamraw.PageContentType.FIGURE))
            continue
        if iterable(index, lists):
            result.append((index, iamraw.PageContentType.LIST))
            continue
        if isformula(index, formula):
            result.append((index, iamraw.PageContentType.FORMULA))
            continue
        if iscaption(index, captions):
            result.append((index, iamraw.PageContentType.CAPTION))
            continue
        if isblockquote(index, blockquotes):
            result.append((index, iamraw.PageContentType.BLOCKQUOTE))
            continue
    return iamraw.PageContentContentType(page=ptcn.page, content=result)


def iterable(line: int, listinstances: set) -> bool:
    if not listinstances:
        return False
    return line in listinstances


def isblockquote(line, quotes):
    if not quotes:
        return False
    if not quotes.content:
        return False
    quotes = quotes.content
    if any(line in area for area, _ in quotes):
        return True
    return False


def isformula(line, formulas):
    if not formulas:
        return False
    if not formulas.content:
        return False
    formulas = formulas.content
    lines = [
        # support multiple line formulas
        utilo.rtuple(
            item.line,
            utilo.ifnone(item.lineend, default=item.line) + 1,
        ) for item in formulas if item.line is not None
    ]
    lines = utilo.flat(lines)
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
    if any(
            utilo.rect_inside(table.bounding, line.bounding, diff=5.0)
            for table in tables.content):
        return True
    return False


def isfigure(line, figures):
    if not figures:
        return False
    if not figures.content:
        return False
    if any(
            utilo.rect_inside(
                figure.bounding,
                line.bounding,
            ) for figure in figures.content):
        return True
    return False


def expand_multiline(captions: iamraw.Captions) -> set:
    lines = [utilo.rtuple(item.line, item.lineend + 1) for item in captions]
    lines = [item for item in lines if item]
    lines = utilo.flat(lines)
    # make unique
    lines = set(lines)  # pylint:disable=R0204
    return lines


def expand_lists(lists):
    """Determine lines which are covered by lines. Expand lists which
    are expanded over more than one page."""
    collect = collections.defaultdict(set)
    for page in lists:
        for listi in page.content:
            areas = listi.area
            areas = areas if isinstance(areas[0], tuple) else [areas]
            for index, area in enumerate(areas, start=page.page):
                collect[index].update(area)
    # enable KeyError
    result = dict(collect)
    return result
