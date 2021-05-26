# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Caption Processor
=================

The caption processor is a very simple approach to collect text after
and before images, figures, tables etc. In the current approach some
text(`look_backward`, `look_forward`) is scanned for `KEYWORDS`.

In the current state it is not possible to ensure that collecting
`steals` the text of an other text item. Duplicated parsing is already
handled correctly."""

import abc

import iamraw
import texmex
import utila

import caption.utils


class CaptionPageProcessor:
    # TODO: ADD CAPTION PROCESSOR WITHOUT KEYWORDS

    def __init__(self, look_backward: int, look_forward: int):
        self.look_forward = look_forward
        self.look_backward = look_backward

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
            y0, y1 = bounding[1], bounding[3]
            selected = self.validate(after(page, y1, self.look_forward))
            if not selected:
                selected = self.validate(before(page, y0, self.look_backward))
            if not selected:
                utila.info(f'could not find caption after: {bounding}')
                continue
            raw = ''.join([item[1].text for item in selected]).strip()
            item = iamraw.Caption(
                line=selected[0][0],
                lineend=selected[-1][0],
                raw=raw,
            )
            result.append(item)
        return result

    @abc.abstractmethod
    def validate(self, items):
        pass


def before(navigator, current, minus):
    selected = [(index, item)
                for index, item in enumerate(navigator)
                if current - minus <= item.bounding.y1 <= current]
    return selected


def after(navigator, current, plus):
    selected = [(index, item)
                for index, item in enumerate(navigator)
                if current <= item.bounding.y1 <= current + plus]
    return selected


class CaptionPageWordProcessor(CaptionPageProcessor):

    def __init__(self, words):
        super().__init__(
            look_backward=150,
            look_forward=150,
        )  # TODO: HOLY VALUE
        self.words = words

    def validate(self, items) -> list:
        matched = [
            item for item in items
            if any(chunk in item[1].text for chunk in self.words)
        ]
        if not matched:
            return []
        textsize = matched[0][1].style.textsize()
        # extend matching by equal font size.
        # TODO: IMPROVE THIS SIMPLE APPROACH
        result = [
            item for item in items
            if item in matched or item[1].style.textsize() == textsize
        ]
        return result


def run(processor, ptcns, items):
    result = []
    for page in ptcns:
        pagefigure = utila.select_page(items, page.page)
        pagefigure = caption.utils.sorted_bounds(pagefigure)
        processed = processor.process_page(page, pagefigure)
        processed = utila.make_unique(processed)
        result.append(
            iamraw.PageContentCaption(
                page=page.page,
                content=processed,
            ))
    return result
