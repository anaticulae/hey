# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
TODO:
    - support table of figures
              table of abbreviation
"""
from typing import List

from iamraw import Document
from serializeraw import dump_likelihood
from serializeraw import load_document
from utila import uniform_result


def work(text_linewise: str) -> str:
    document = load_document(text_linewise)

    extracted = extract_toc_likelihood(document)
    dumped = dump_likelihood(extracted)
    return dumped


def extract_toc_likelihood(document: Document) -> List[float]:
    """Iterate throw the document and determine the uniformed likelihood of
    beeing a table page

    Returns:
        uniformed likelihood list with probabilty of beeing a table page
    """
    result = [analyse_page(page) for page in document]
    uniformed = uniform_result(result)
    return uniformed


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

    possible_toc_line = len([line for line in content if line.count('. .') > 3])

    # likelihood = possible_toc_line / linecount if linecount else 0.0
    return linecount, possible_toc_line
