# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import abc

import iamraw
import texmex
import utila

import caption.utils


class CaptionPageProcessor:

    def __init__(self, look_forward: int):
        self.look_forward = look_forward

    def process_page(
            self,
            page: texmex.PageTextContentNavigator,
            items,
    ) -> iamraw.Captions:
        """Detect caption below the images."""
        if not items:
            return []
        result = []
        for bounding in items:
            y1 = bounding[3]
            selected = self.after(page, y1)
            if not selected:
                utila.info(f'could not find caption after: {bounding}')
                continue
            raw = ''.join([item[1].text for item in selected]).strip()
            line, _ = selected[0]
            lineend, _ = selected[-1]
            item = iamraw.Caption(line=line, lineend=lineend, raw=raw)
            result.append(item)
        return result

    @abc.abstractmethod
    def validate(self, items):
        pass

    def after(self, navigator, current):
        plus = self.look_forward
        selected = [(index, item)
                    for index, item in enumerate(navigator)
                    if current <= item.bounding.y1 <= current + plus]
        # TODO: IMPROVE THIS SIMPLE SELECTOR
        valid = self.validate(selected)
        return valid


class CaptionPageWordProcessor(CaptionPageProcessor):

    def __init__(self, words):
        super().__init__(look_forward=150)  # TODO: HOLY VALUE
        self.words = words

    def validate(self, items) -> list:
        result = [
            item for item in items
            if any(chunk in item[1].text for chunk in self.words)
        ]
        if not result:
            return result
        textsize = result[0][1].style.textsize()
        # extend matching by equal font size.
        # TODO: IMPROVE THIS SIMPLE APPROACH
        matched = [
            item for item in items
            if item in result or item[1].style.textsize() == textsize
        ]
        return matched


def run(processor, ptcns, items):
    result = []
    for page in ptcns:
        pagefigure = utila.select_page(items, page.page)
        pagefigure = caption.utils.sorted_bounds(pagefigure)
        processed = processor.process_page(page, pagefigure)
        result.append(
            iamraw.PageContentCaption(
                page=page.page,
                content=processed,
            ))
    return result
