# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from re import X
from re import compile as recompile
from re import match
from typing import List

from iamraw import Document
from serializeraw import load_document

from sections.feature import uniform_result


def work(text_linewise: str, pagenumbers: str) -> str:
    # TODO: Share resources
    document = load_document(text_linewise)
    extract_index_likelihood(document)


def extract_index_likelihood(document: Document) -> List[float]:
    result = [analyse_page(page) for page in document]
    uniformed = uniform_result(result)
    return uniformed


def analyse_page(page) -> float:
    content = page.text.splitlines()
    linecount = len(content)

    single_char = [
        item for item in content if len(item) == 1 and item.isalpha()
    ]

    # INDEX, PAGENUMBER
    pattern = recompile(
        r"""^([a-zA-Z]+\s?){1,3}
                    [\s|,]?
                    \s{0,5}
                    [0-9]+$
                """, X)
    index_with_page = [line for line in content if match(pattern, line)]
    for item in index_with_page:
        print(item)
    single_char_or_index_with_page = len(single_char) + len(index_with_page)

    return linecount, single_char_or_index_with_page
