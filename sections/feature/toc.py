# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
TODO:
    - support table of figures
              table of abbreviation
"""
import typing

import iamraw
import serializeraw

import sections
import sections.feature


def work(text_linewise: str, pages=None) -> str:
    document = serializeraw.load_document(text_linewise, pages=pages)

    extracted = extract_toc_likelihood(document)
    dumped = serializeraw.dump_likelihood(extracted)
    return dumped


def extract_toc_likelihood(document: iamraw.Document) -> typing.List[float]:
    """Iterate throw the document and determine the uniformed likelihood of
    beeing a table page

    Returns:
        uniformed likelihood list with probabilty of beeing a table page
    """

    result = {page.page: analyse_page(page) for page in document}

    # NO TOC AFTER PAGE 30: TODO: HOLY VALUE
    result = {
        page: value if page < 30 else (0, 0) for page, value in result.items()
    }

    uniformed = sections.feature.uniform_result(result)
    multiformed = sections.feature.multiform_result(result)
    if multiformed is not None:
        uniformed = multiformed
    assert len(uniformed) == len(document)

    result = [
        iamraw.PageContentLikelihood(
            page=page, content=iamraw.Likelihood(value, 'toc'))
        for page, value in uniformed.items()
    ]
    result = sorted(result, key=lambda x: x.page)
    return result


def analyse_page(page) -> float:
    """Extract the number of lines which can be contain any table-content

    Dots(. . .) are charactaristical for table lines.

    Args:
        page():
    Returns:
        (linecount, possible_table_lines)
    """
    content = page.text.splitlines()
    linecount = len(content)

    possible_toc_line = len([
        line for line in content
        if line.count('. .') > 3 or line.count('..') > 3
    ])

    # likelihood = possible_toc_line / linecount if linecount else 0.0
    return linecount, possible_toc_line
