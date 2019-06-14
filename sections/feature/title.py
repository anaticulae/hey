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


class TextContainerIterator:

    def __init__(self, page):
        # TODO: We do not want to copy!
        self.page = [item for item in page if isinstance(item, TextContainer)]

    def __getitem__(self, index):
        return self.page[index]

    def __len__(self):
        return len(self.page)


class PageIter:
    # Contenxt Manager?
    def __init__(self, page):
        self.page = TextContainerIterator(page)
        self.container = 0
        self.line = 0
        self.char = 0

    def next(self, container, line, char):
        result = ''

        if self.line > 0 and self.container < container:
            # Fill up the container before continuing with the next
            for item in self.page[self.container][self.line:]:
                result += item.text
            self.line = 0
            self.container += 1

        while self.container < container:
            result += self.page[self.container].text
            self.container += 1
        while self.line < line:
            result += self.page[self.container][self.line].text
            self.line += 1
        return result

    def finish(self):
        return self.next(len(self.page), 0, 0)


def split_page(page: Page, positions: List) -> List[str]:
    """Split page into chunks given by `positions`. The source of these
    positions can be rawmaker with font-extractor, ..., .

    page(Page): page with text content(TextContainer)
    positions(List[(container, line, char)]): List with separation order

    Returns:
        List[str]: text content of chunk
    """
    pageiter = PageIter(page=page)
    result = [pageiter.next(*item).strip() for item in positions]
    finish = pageiter.finish().strip()
    if finish:
        result.append(finish)
    return result


MINIMAL_TITLE_LENGTH = 10
MAXIMAL_TITLE_LENGTH = 200


def analyse_page(page: Page, fontstore: FontLookUp) -> float:
    # TODO: -1, investigate, why page number does not start with zero!
    number = page.number - 1
    positions = [(
        container,
        line,
        char,
    ) for container, line, char, _ in fontstore.page_iter(number)]

    fonts = [
        fontstore.fromindex(font).scale
        for _, __, ___, font in fontstore.page_iter(number)
    ]
    if not fonts:
        return 1, 0.0

    max_font = max(fonts)
    max_font_index = fonts.index(max_font)

    text_length = [len(item) for item in split_page(page, positions)]
    max_font_length = text_length[max_font_index]

    value = 0
    if MINIMAL_TITLE_LENGTH <= max_font_length < MAXIMAL_TITLE_LENGTH:
        value = max_font_length * pow(max_font, 3)
    # Malus per page, reduce value 5% per page, the higher the page number
    # the lower the likelihood to be the title page.
    value = value * pow(0.95, number)
    return max_font_length, value
