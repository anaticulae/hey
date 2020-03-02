# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Likelihood Detection
=================================

Currently there are two different approaches to differentiate between
abbreviation and non abbreviation pages. On the first side we check that
there are not to much sentences on a page. On the other side we search
for selective words "Abkuerzungsverzeichnis, ...".

NOTE: This approach is only for demo time.
"""

import typing

import iamraw
import serializeraw
import texmex
import utila

import sections.feature
import sections.utils.text

TITLE = ['Abkürzungsverzeichnis']

# TODO: REPLACE
PageResult = typing.Tuple[texmex.Occurrence, int]  # number


def work(document: str, position: str, pages=None) -> str:
    # load and setup
    pages = tuple(pages) if pages else None
    document = serializeraw.load_document(document, pages=pages)
    position = serializeraw.load_textpositions(position, pages=pages)

    navigators = texmex.create_pagetextnavigators(
        text=document,
        text_positions=position,
        # fill_empty=False,
    )
    # TODO: REMOVE AFTER UPGRADING IAMRAW, add fill_empty=False
    navigators = [
        item for item in navigators if not utila.should_skip(item.page, pages)
    ]

    result = {page.page: analyse_page(page) for page in navigators}

    uniformed = sections.feature.uniform_result(result)

    likelihood = [
        iamraw.PageContentLikelihood(
            page=page,
            content=iamraw.Likelihood(value, 'abbreviation_table'),
        ) for page, value in uniformed.items()
    ]

    # write result
    dumped = serializeraw.dump_likelihood(likelihood)
    return dumped


def analyse_page(navigator: texmex.PageTextNavigator) -> PageResult:
    result = []
    if not is_abbreviation_table_statistical(navigator):
        return (0, 0.0)

    for line in navigator:
        line = line.text.strip()
        if line in TITLE:
            result.append(line)

    if not result:
        # could not find any TITLE line
        return (0, 0)
    return (len(result), 1.0)


def is_abbreviation_table_statistical(navigator: texmex.PageTextNavigator):
    textonpage = sections.utils.text.textonpage(navigator)
    if len(textonpage.sentences) > 5:
        # TODO: HOLY VALUE
        return False
    return True
