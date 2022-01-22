# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import configo
import iamraw
import texmex
import utila


class CaptionPageProcessor:
    # TODO: ADD CAPTION PROCESSOR WITHOUT KEYWORDS

    def __init__(self, look_backward: int, look_forward: int):
        self.look_forward = look_forward
        self.look_backward = look_backward

    def process_page(
        self,
        page: texmex.PageTextContentNavigator,
        boundings,
    ) -> iamraw.Captions:
        """Detect caption after and before boundings."""
        if not boundings:
            return []
        result = []
        for bounding in boundings:
            y0, y1 = bounding[1], bounding[3]
            selected = self.validate_after(items=after(
                page,
                y1,
                self.look_forward,
            ))
            if not selected:
                selected = self.validate_before(items=before(
                    page,
                    y0,
                    self.look_backward,
                ))
            if not selected:
                utila.info(f'could not find caption for: {bounding}')
                continue
            raw = ''.join([item[1].text for item in selected]).strip()
            item = iamraw.Caption(
                line=selected[0][0],
                lineend=selected[-1][0],
                raw=raw.strip(),
            )
            result.append(item)
        return result

    @abc.abstractmethod
    def validate_after(self, items):
        pass

    @abc.abstractmethod
    def validate_before(self, items):
        pass


def before(navigator, current, minus):
    start = current - minus
    result = []
    for index, item in enumerate(navigator):
        center = (item.bounding.y0 + item.bounding.y1) / 2
        if start <= center <= current:
            result.append((index, item))
    return result


def after(navigator, current, plus):
    end = current + plus
    result = []
    for index, item in enumerate(navigator):
        center = (item.bounding.y0 + item.bounding.y1) / 2
        if current <= center <= end:
            result.append((index, item))
    return result


def diffs(items):
    result = []
    boundings = [[item[1].bounding.y1, item[1].bounding.y0] for item in items]
    for current, nexxt in zip(boundings[0:-1], boundings[1:]):
        diff = nexxt[0] - current[1]
        result.append(diff)
    return result


CAPTION_LOOK_BACKWARD_MAX = configo.HV_FLOAT_PLUS(default=150)

CAPTION_LOOK_FORWARD_MAX = configo.HV_FLOAT_PLUS(default=150)

CAPTION_LINE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=30.0)


class CaptionPageWordProcessor(CaptionPageProcessor):

    def __init__(self, words):
        super().__init__(
            look_backward=CAPTION_LOOK_BACKWARD_MAX,
            look_forward=CAPTION_LOOK_FORWARD_MAX,
        )
        self.words = words

    def validate_after(self, items) -> list:
        end = len(items)
        diffed = diffs(items)
        for index, item in enumerate(diffed):
            # split potential caption by maximum text line space
            if item > CAPTION_LINE_DIFF_MAX:
                end = index + 1
                break
        content = items[0:end]
        for index, line in enumerate(content):
            if any(utila.match(pat, line[1].text) for pat in self.words):
                return content[index:]
        return []

    def validate_before(self, items) -> list:
        selected = None
        for index, item in enumerate(items):
            if any(utila.match(pat, item[1].text) for pat in self.words):
                selected = index
        if selected is None:
            # nothing matched
            return []
        result = items[selected:]
        result = inside(result)
        return result


def inside(lines: list) -> list:
    """Verify that possible other caption lines are inside caption
    [x0,x1] bounding and have the same textsize.
    """
    if not lines:
        return []
    x0 = lines[0][1].bounding.x0 - 50
    x1 = lines[0][1].bounding.x1 + 50
    # TODO: IMPROVE THIS SIMPLE APPROACH
    textsize = lines[0][1].style.textsize()
    result = [lines[0]]
    for line in lines[1:]:
        current = line[1].style.textsize()
        bbox = line[1].bounding
        if current == textsize and x0 <= bbox.x0 <= bbox.x1 < x1:
            result.append(line)
        else:
            break
    return result


def run(processor, ptcns, items):
    result = []
    for page in ptcns:
        pagefigure = utila.select_page(items, page.page)
        if not pagefigure:
            continue
        # determine and sort boundings of captionized figure/table/...
        boundings = [item.bounding for item in pagefigure.content]
        boundings = utila.sort_leftright_topdown(boundings)
        # determine captions
        processed = processor.process_page(page, boundings)
        processed = utila.make_unique(processed)
        captions = iamraw.PageContentCaption(
            page=page.page,
            content=processed,
        )
        result.append(captions)
    return result
