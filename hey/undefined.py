# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw import Border

from hey.textnavigator.navigator import PageTextContentNavigator
from hey.textnavigator.navigator import create_pagetextnavigators


def extract_undefined(pages, text, text_position, contentborder):
    """Fill `undefined items` with TextContent and BoundingBox

    Args:
        pages(int)
        text():
        text_position:
        border(Border): contentborder which is equal for the whole document
    Returns:
        replaced pages with grouped replaced undefined items
    """
    assert isinstance(contentborder, Border), type(contentborder)
    pagetextnavigators = create_pagetextnavigators(
        text=text,
        text_position=text_position,
    )
    result = []
    for (page, pagecontent) in pages:
        # TODO: do not always create a new pcn
        ptcn = PageTextContentNavigator(pagetextnavigators[page], contentborder)
        _pagecontent = []
        for index, (_, paragraph) in enumerate(pagecontent):
            # split the undefined groups
            splitted_paragraph = splitter(paragraph)
            # fill undefined groups with text content
            paragraph_items = [(uindex, [
                ptcn[int(item[:-1])] for item in undefineds
            ]) for (uindex, undefineds) in enumerate(splitted_paragraph)]

            if paragraph_items:
                _pagecontent.append((
                    page,
                    index,
                    paragraph_items,
                ))
        result.append(_pagecontent)
    return result


def splitter(items):
    """Create groups of undefined items separated by content items"""
    result, current = [], []
    for item in items:
        try:
            _, char = int(item[0:-1]), item[-1]
            if char != 'u':
                continue
            current.append(item)
        except ValueError:
            if current:
                result.append(current)
                current = []
    if current:
        result.append(current)
    return result
