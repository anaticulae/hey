# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from re import match
from typing import List

from iamraw import Document
from iamraw import Page

from groupme.feature import HEADLINE
from groupme.feature import create_raw
from groupme.feature import format_title


def header(document: Document) -> str:
    from groupme.feature.toc import toc
    tableofcontent = toc(document)
    if not tableofcontent:
        # No toc in document
        return None
    # Split content from header due first headline
    first_headline = format_title(tableofcontent[0])
    splitted = document.text.rsplit(first_headline, 1)
    # print('Splitted')
    # # print(splitted)
    # print('Start')
    # print(first_headline)
    # print(splitted[0])
    # print('End')
    # print(splitted)
    # TODO: We need a better algorithmn
    # Detect toc-page and split after
    assert len(splitted[0]) > 300  # front page, toc etc.
    return splitted[0]


def body(document: Document) -> str:
    header_ = header(document)
    result = document.text.split(header_)[1]
    return result


def sections(document: Document) -> List[str]:
    """Determine `sections` from `Document`"""
    result = []
    for page in document.pages:
        result.extend(sections_from_page(page))
    return result


def sections_from_page(page: Page) -> List[str]:
    """Parse headline due regex `HEADLINE` from `Page

    Args:
        page(Page): one page of `Document`
    Returns:
        List[str] of potential headlines
    """
    result, headline, text = [], None, []
    for line in page.text.splitlines():
        parsed = parse_headline(line)
        if parsed:
            if text or headline:
                result.append(create_raw(headline, text))
            headline = parsed
            text = []
        else:
            text.append(line)
    if text:
        result.append(create_raw(headline, text))
    return result


def parse_headline(line: str):
    """Extract potential headline from str

    Use regex to determine headlines with level in document from random text.
    In some cases this will not work, for example:

    ```
        CHAPTER 3
        RestructuredText Customizations
    ```

    Args:
        line(str): random text line of document
    Returns
        (level, title): return potential level/depth and title of headline
    """
    assert isinstance(line, str)
    matched = match(HEADLINE, line)
    if not matched:
        return None
    level = matched['level']
    if len(level) <= 2 and level[0].islower():
        return None
    return (level, matched['title'])
