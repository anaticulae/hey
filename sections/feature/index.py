# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from re import X
from re import compile as recompile
from re import match
from typing import Tuple

import iamraw
import serializeraw

import sections


def work(text_linewise: str, pages=None) -> str:
    """Load document and extract likelihood of beening an index page

    Args:
        text_linewise(str): path to document with high `char_margin`
    Returns:
        yaml content with dumped result for every single page
    """
    document = serializeraw.load_document(text_linewise, pages=pages)
    extracted = extract_index_likelihood(document)
    dumped = serializeraw.dump_likelihood(extracted)
    return dumped


def extract_index_likelihood(document: iamraw.Document,
                            ) -> iamraw.PageContentLikelihoods:
    """Extract likelihood of beeing an index page. Determine a likelihood for
    every single page.

    Args:
        document(Document): document to iterate over single pages
    Returns:
        a normalized List[float] with the normalized likelihood of beeing an
        index page
    """
    result = {page.page: analyse_page(page) for page in document}

    uniformed = sections.feature.uniform_result(result)
    assert len(uniformed) == len(document)

    result = [
        iamraw.PageContentLikelihood(
            page=page, content=iamraw.Likelihood(value, 'index'))
        for page, value in uniformed.items()
    ]
    result = sorted(result, key=lambda x: x.page)
    return result


# INDEX, PAGENUMBER
INDEX_ITEM_PATTERN = recompile(
    r"""^([a-zA-Z]+\s?){1,3} # one till three words
          [\s|,]?            # optional `,`
          \s{0,5}            # between zero and five spaces
          [0-9]+$            # a pagenumber at the end
     """, X)

MINIMAL_DETECTED_PATTERN_PERCENT = 0.4  # TODO: HOLY VALUE


def analyse_page(page: iamraw.Page) -> Tuple[int, int]:
    """Extract potential features of an index page

    This methods search for 2 features. The simpelst feature is a single
    char. This char represents the index A-Z. The second feature is a pattern
    out of index-name and index-page.

    Args:
        page(Page): page to search for index features
    Returns:
        (linecount, matched features):
    """
    content = page.text.splitlines()
    # remove empty lines
    content = [item for item in content if item]
    linecount = len(content)

    # search for single chars, which represents the index
    single_char = [
        item for item in content if len(item) == 1 and item.isalpha()
    ]

    index_with_page = [
        line for line in content if match(INDEX_ITEM_PATTERN, line)
    ]
    single_char_or_index_with_page = len(single_char) + len(index_with_page)

    percent = single_char_or_index_with_page / linecount if linecount else 0

    if percent < MINIMAL_DETECTED_PATTERN_PERCENT:
        linecount = 0
        single_char_or_index_with_page = 0

    return linecount, single_char_or_index_with_page
