# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from typing import List

import iamraw
from serializeraw import dump_likelihood
from serializeraw import load_document

import sections.textprocessor
from hey.fonts.store import FontStore
from hey.fonts.store import create_fontstore


def work(
        text_linewise: str,
        font_header: str,
        font_content: str,
        pages=None,
) -> str:
    document = load_document(text_linewise, pages=pages)

    lookup = create_fontstore(font_header, font_content)

    result = extract_title_likelihood(document, lookup)
    dumped = dump_likelihood(result)
    return dumped


def extract_title_likelihood(
        document: iamraw.Document,
        fontstore: FontStore,
) -> List[float]:
    result = {page.page: analyse_page(page, fontstore) for page in document}

    uniformed = sections.feature.uniform_result(result)

    result = [
        iamraw.PageContentLikelihood(
            page=page,
            content=iamraw.Likelihood(value, 'title'),
        ) for page, value in uniformed.items()
    ]
    return result


MINIMAL_TITLE_LENGTH = 10
MAXIMAL_TITLE_LENGTH = 200

EMPTY_RESULT = (0, 0.0)


def analyse_page(page: iamraw.Page, fontstore: FontStore) -> float:
    """Determine the likelihood that `page` is a title page

    A high title_indicator provides a high likelihood of beeing a title
    page. Aditionally the max_font_length is provided.

    Args:
        page(Page):
        fontstore(FontStore):
    Returns:
        (max_font_length, title_indicator):
    """
    pagenumber = page.page
    positions = font_positions_from_page(fontstore, pagenumber)
    fonts = font_sizes_from_page(fontstore, pagenumber)

    if not fonts:  # empty page or page with images
        return EMPTY_RESULT

    max_font, max_font_length = determine_hugest_font(fonts, positions, page)
    title_indicator = 0
    # the title must not be to short and it unlikeli that the title is very,
    # very long.
    # TODO: We need a concept for this "holy" values. Make them configurable
    if MINIMAL_TITLE_LENGTH <= max_font_length < MAXIMAL_TITLE_LENGTH:
        title_indicator = max_font_length * pow(max_font, 3)
    # Malus per page, reduce value 10% per page, the higher the page number
    # the lower the likelihood to be the title page.
    # TODO: investigate if this is a good idea
    title_indicator = title_indicator * pow(0.10, pagenumber)
    return max_font_length, title_indicator


def font_sizes_from_page(store: FontStore, pagenumber: int):
    fonts = [
        store[font].scale for _, __, ___, font in store.page_iter(pagenumber)
    ]
    return fonts


def font_positions_from_page(store: FontStore, pagenumber: int):
    positions = [(
        container,
        line,
        char,
    ) for container, line, char, _ in store.page_iter(pagenumber)]
    return positions


def determine_hugest_font(fonts, positions, page: iamraw.Page):
    # determine the biggest font size
    max_font = max(fonts)
    max_font_index = fonts.index(max_font)

    text_length = [
        len(item)
        for item in sections.textprocessor.split_page(page, positions)
    ]
    max_font_length = text_length[max_font_index]
    return max_font, max_font_length
