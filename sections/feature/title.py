# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from typing import List

from iamraw import Document
from iamraw import Page
from iamraw import TextContainer
from serializeraw import load_document

from sections.feature import uniform_result
from sections.font import FontLookUp


def work(text_linewise: str, pagenumbers: str) -> str:
    # TODO: Share resources
    document = load_document(text_linewise)
    extract_index_likelihood(document)


def extract_title_likelihood(
        document: Document,
        fontstore: FontLookUp,
) -> List[float]:
    result = [analyse_page(page, fontstore) for page in document]
    uniformed = uniform_result(result)
    return uniformed


MINIMAL_TITLE_LENGTH = 10
MAXIMAL_TITLE_LENGTH = 200

EMPTY_RESULT = (0, 0.0)


def analyse_page(page: Page, fontstore: FontLookUp) -> float:
    number = page.number

    positions = font_positions_from_page(fontstore, number)
    fonts = font_sizes_from_page(fontstore, number)

    if not fonts:  # empty page or page with images
        return EMPTY_RESULT

    max_font, max_font_length = determine_hugest_font(fonts, positions, page)
    value = 0
    # the title must not be to short and it unlikeli that the title is very,
    # very long.
    # TODO: We need a concept for this "holy" values. Make them configurable
    if MINIMAL_TITLE_LENGTH <= max_font_length < MAXIMAL_TITLE_LENGTH:
        value = max_font_length * pow(max_font, 3)
    # Malus per page, reduce value 10% per page, the higher the page number
    # the lower the likelihood to be the title page.
    # TODO: investigate if this is a good idea
    value = value * pow(0.10, number)
    return max_font_length, value


def font_sizes_from_page(store: FontLookUp, pagenumber: int):
    fonts = [
        store.fromindex(font).scale
        for _, __, ___, font in store.page_iter(pagenumber)
    ]
    return fonts


def font_positions_from_page(store: FontLookUp, pagenumber: int):
    positions = [(
        container,
        line,
        char,
    ) for container, line, char, _ in store.page_iter(pagenumber)]
    return positions


def determine_hugest_font(fonts, positions, page: Page):
    # determine the biggest font size
    max_font = max(fonts)
    max_font_index = fonts.index(max_font)

    text_length = [len(item) for item in split_page(page, positions)]
    max_font_length = text_length[max_font_index]
    return max_font, max_font_length
