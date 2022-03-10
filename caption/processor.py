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
import itertools

import configo
import iamraw
import texmex
import utila


class CaptionPageProcessor:
    # TODO: ADD CAPTION PROCESSOR WITHOUT KEYWORDS

    def __init__(
        self,
        look_backward: int,
        look_forward: int,
        typ: iamraw.CaptionType = None,
        verbose: bool = False,
    ):
        self.look_forward = look_forward
        self.look_backward = look_backward
        self.typ = typ
        self.verbose = verbose

    def process_page(
        self,
        page: texmex.PageTextContentNavigator,
        boundings,
        page_next: texmex.PageTextContentNavigator = None,
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
            overlap = False
            if not selected:
                selected = self.search_pageafter(y1, page, page_next)
                if selected:
                    overlap = True
            if not selected:
                utila.info(f'could not find caption for: {bounding}')
                continue
            item = self.create_caption(selected, overlap=overlap)
            result.append(item)
        return result

    def search_pageafter(self, y1, page, page_next):
        if not page_next:
            return None
        overlap_check = page.height * CAPTION_NEXT_PAGE
        if y1 < overlap_check:
            return None
        # look on page after
        selected = self.validate_after(items=after(
            page_next,
            current=CAPTION_NEXT_PAGE_CONTENT_START,
            plus=self.look_forward,
        ))
        return selected

    def create_caption(self, selected, overlap: bool = False) -> iamraw.Caption:
        if self.verbose:
            selected, matched = selected
        raw = '\n'.join([item[1].text for item in selected])
        raw = utila.normalize_text(raw)
        item = iamraw.Caption(
            line=selected[0][0],
            lineend=selected[-1][0],
            typ=self.typ,
            overlap=overlap,
            raw=raw,
        )
        if self.verbose:
            item.label = matched[1]
            item.number = matched[2]
            item.text = raw[matched.end():].strip()
        return item

    @abc.abstractmethod
    def validate_after(self, items):
        pass

    @abc.abstractmethod
    def validate_before(self, items):
        pass


# Bounding is on the bottom of the page. We do not check the next page for
# objects at the top of the page.
CAPTION_NEXT_PAGE = configo.HV_PERCENT_PLUS(default=80)
# skip header content
CAPTION_NEXT_PAGE_CONTENT_START = configo.HV_INT_PLUS(default=50)


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


CAPTION_LOOK_BACKWARD_MAX = configo.HV_FLOAT_PLUS(default=120)

CAPTION_LOOK_FORWARD_MAX = configo.HV_FLOAT_PLUS(default=150)

CAPTION_LINE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=30.0)


class CaptionPageWordProcessor(CaptionPageProcessor):

    def __init__(
        self,
        words,
        typ: iamraw.CaptionType = None,
        verbose: bool = True,
    ):
        super().__init__(
            look_backward=CAPTION_LOOK_BACKWARD_MAX,
            look_forward=CAPTION_LOOK_FORWARD_MAX,
            typ=typ,
            verbose=verbose,
        )
        self.words = words if utila.iterable(words) else (words,)

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
            for pattern in self.words:
                matched = pattern.match(line[1].text)
                if not matched:
                    continue
                if not self.verbose:
                    return content[index:]
                return content[index:], matched
        return []

    def validate_before(self, items) -> list:
        selected = None
        matched = None
        for index, item in enumerate(items):
            for pattern in self.words:
                checked = pattern.match(item[1].text)
                if not checked:
                    continue
                selected = index
                matched = checked
        if selected is None:
            # nothing matched
            return []
        result = items[selected:]
        result = inside(result)
        if not self.verbose:
            return result
        return result, matched


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
    for page, pageafter in itertools.zip_longest(ptcns, ptcns[1:]):
        pagefigure = utila.select_page(items, page.page)
        if not pagefigure:
            continue
        # determine and sort boundings of captionized figure/table/...
        boundings = [item.bounding for item in pagefigure.content]
        boundings = utila.sort_leftright_topdown(boundings)
        # determine captions
        processed = processor.process_page(page, boundings, page_next=pageafter)
        processed = utila.make_unique(processed)
        for item in processed:
            item.pdfpage = page.page
        captions = iamraw.PageContentCaption(
            page=page.page,
            content=processed,
        )
        result.append(captions)
    return result
