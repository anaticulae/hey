# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import List

from iamraw import Page
from iamraw import TextContainer


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
        empty = True
        result = ''
        if all([
                container == self.container,
                line == self.line,
                char == self.char,
        ]):
            raise ValueError('iter stands on goal %d %d' % (container, line))

        if self.char > 0 and char == 0:
            # text iterator is not on the line start
            if self.container < container or self.line < line:
                # fill the rest of the current line and goto next lien
                result += self.page[self.container][self.line].text[self.char:]
                self.char = 0
                self.line += 1
                empty = False
        if self.line > 0 and self.container < container:
            # Fill up the container before continuing with the next
            for item in self.page[self.container][self.line:]:
                result += item.text
                empty = False
            self.line = 0
            self.container += 1
        while self.container < container:
            result += self.page[self.container].text
            self.container += 1
            empty = False
        while self.line < line:
            result += self.page[self.container][self.line].text
            self.line += 1
            empty = False
        if char:
            result += self.page[self.container][self.line].text[self.char:char]
            # Example: iterator stands on 10, next `char` is 15, we have to add
            # chardistance (15-10) to add. After this the current iterator
            # stands on 15.
            charsdistance = (char - self.char)
            self.char += charsdistance
            empty = False

        if empty:
            msg = 'no content selected %d %d %d' % (container, line, char)
            raise ValueError(msg)
        return result

    def finish(self):
        # TODO Dirty hack!
        try:
            return self.next(len(self.page), 0, 0)
        except ValueError:
            return ''


def split_page(page: Page, positions: List) -> List[str]:
    """Split page into chunks given by `positions`. The source of these
    positions can be rawmaker with font-extractor, ..., .

    Args:
        page(Page): page with text content(TextContainer)
        positions(List[(container, line, char)]): List with separation order

    Returns:
        List[str]: text content of chunks
    """
    pageiter = PageIter(page=page)
    result = [pageiter.next(*item).strip() for item in positions]
    finish = pageiter.finish().strip()
    if finish:
        result.append(finish)
    return result
