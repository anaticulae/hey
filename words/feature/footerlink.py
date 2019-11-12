# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Example:

* high notes: ^1 ^2 ^3

"""

import hey.textnavigator.style
import words.feature
import words.text
import words.text.chapter
import words.text.sentence


def work() -> str:
    pass


def extract_highnotes(loaded: words.feature.TextRequiredResources,
                     ) -> words.text.PageContentPageTextDetecteds:
    """Iterate thrue document via headline and process the content
    between the headlines. Split Chapter into paragraphs and paragraphs
    into sentences and words.

    Args:
        loaded: resources provided by text module
    Returns:
        list of text pages with textutal content definition
    """
    loaded = words.text.chapter.split(loaded)

    result = []
    for page in loaded:
        for headline, content in words.text.sentence.visit_sections(page):
            highnotes = hey.textnavigator.style.highnotes(content)
            result.extend(highnotes)
    return result
