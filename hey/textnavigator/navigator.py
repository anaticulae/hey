# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os
from typing import List
from typing import Tuple

import serializeraw
from iamraw import Border
from iamraw import BoundingBox
from iamraw import Document
from iamraw import PageSize
from iamraw import common_box
from utila import NEWLINE

from hey.textnavigator.fonts import TextBoundsList
from hey.textnavigator.fonts import feeddistance
from hey.textnavigator.fonts import fontdistance

START = 0.0
END = 1.0


class PageTextNavigator:
    """The PageTextNavigator eases to navigate through the textual
    content of a Page. The text is processed from top to down and left
    to right.
    """

    def __init__(self, size=None, page=-1):
        """Initialize PageTextNavigator with maximal `size`

        Args:
            size(tuple): maximal width/height of PageTextNavigator
            page(int): page number of PageTextNavigator-instance

        Sizes:
            A4: 210 x 297 mm, 8.26 x 11.69 inch, 595 x 842pt
                                                 612 x 792pt
        """
        if size is None:
            size = (612.0, 792.0)
        self.page = page
        self.data = []
        self.width, self.height = size

    def insert(self, box: BoundingBox, item: str):
        """Insert text element top to bottom and left to right

        Args:
            box(BoundingBox): position and dimension of text area
            item(str): content of text chunk
        """
        x0, y0, x1, y1 = box
        msg = '0<=%d<=%d<=%d'
        assert 0 <= x0 <= x1 <= self.width, msg % (x0, x1, self.width)
        assert 0 <= y0 <= y1 <= self.height, msg % (y0, y1, self.height)

        insert_position = 0
        for pos, _ in self.data:
            if int(pos.y0) == int(y0):
                if int(x0) <= int(pos.x0):
                    break
            elif y0 <= pos.y0:
                break
            insert_position += 1
        self.data.insert(insert_position, (box, item))

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self) -> int:
        """Count text chunks"""
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    @property
    def dimension(self):
        return PageSize(width=self.width, height=self.height)

    def before(self, height: float, width=0.0):
        """Determine elements on the top of the document

        Args:
            height(float[0.0,1.0]): 0.0 is top, 1.0 is bottom
        Returns:
            List[(position, PageObjects)]
        """
        result = self.between(START, height)
        return result

    def between(self, top: float, bottom: float):
        """Return the content between top(0.0) and bottom(1.0) position.

        Args:
            top(float):
            bottom(float):
        Returns:
            List[(position, content)]
        """
        assert START <= top <= bottom <= END, f'{START}<={top}<={bottom}<={END}'
        before = top * self.height
        after = bottom * self.height
        result = []
        for box, item in self.data:
            # before and after are pixel coordinates
            if before <= box.y0 <= box.y1 <= after:
                result.append((box, item))
        return result

    def after(self, height, width=0.0):
        """Determine elements on the bottom of the page"""
        result = self.between(height, END)
        return result

    def offset(self, top: float, bottom: float) -> Tuple[int, int]:
        # """Determine offset
        assert START <= top <= bottom <= END
        after = bottom * self.height
        before = top * self.height  # greater than

        result = []
        for index, (box, _) in enumerate(self.data):
            # before and after are pixel coordinates
            if before <= box.y0 <= box.y1 <= after:
                result.append(index)
        if not result:
            return None, None
        top, bottom = result[0], result[-1] + 1
        return top, bottom

    @classmethod
    def from_str(cls, text: str):
        """Create PageTextNavigator out of text area

        Hint:
            text position is not supported
        """
        result = cls()
        for index, line in enumerate(text.splitlines()):
            result.insert(
                BoundingBox.from_list([0, index * 20, 300, (index + 1) * 20]),
                line,
            )
        return result


class PageTextContentNavigator:
    """Iterate over page content without footer and header.

    See: PageTextNavigator"""

    def __init__(
            self,
            textnavigator: PageTextNavigator,
            content: Border,
    ):
        """Navigate throw text content, ignore footer and header

        Args:
            textnavigator(PageTextNavigator):
            content(Tuple[top,bottom]):
        """
        msg = 'require `PageTextNavigator` got: %s' % type(textnavigator)
        assert isinstance(textnavigator, PageTextNavigator), msg
        msg = 'require `Border` got: %s' % type(content)
        assert isinstance(content, Border), msg
        pagesize = PageSize(
            width=textnavigator.width,
            height=textnavigator.height,
        )
        assert content.bottom >= 100, str(content)  # ensure that are pixel
        top, bottom = topbottom(pagesize, content)
        assert 0 <= top <= bottom <= 1.0, str(top) + str(bottom)
        self.page = textnavigator.page
        self.data = textnavigator.between(top, bottom)
        self._offset = textnavigator.offset(top, bottom)

    @property
    def offset(self):
        return self._offset

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)


PageTextNavigators = List[PageTextNavigator]


def create_pagetextnavigators(
        text: Document,
        text_positions,
) -> PageTextNavigators:
    result = []
    dimension = (text.dimension.width, text.dimension.height)
    for textposition in text_positions:
        navigator = PageTextNavigator(size=dimension, page=textposition.page)
        result.append(navigator)
        textid = 0
        for item in text[textposition.page]:
            # assert item.number == pagenumber, item.number
            try:
                # TODO: Remove strip after container is fixed
                textcontent = item.text.strip()
            except AttributeError:
                # no text element
                continue
            else:
                pos = textposition.content[textid]
                navigator.insert(pos, textcontent)
                textid += 1
    return result


def create_pagetextnavigators_frompath(path: str, pages=None):
    text = os.path.join(path, 'rawmaker__text_text.yaml')
    text = serializeraw.load_document(text, pages=pages)

    text_position = os.path.join(path, 'rawmaker__text_positions.yaml')
    text_position = serializeraw.load_textpositions(text_position, pages=pages)

    navigators = create_pagetextnavigators(text, text_position)
    return navigators


def topbottom(size: PageSize, contentborder: Border):
    height = size.height
    top, bottom = contentborder.top, contentborder.bottom
    top = percent_from_pagesize(height, top)
    bottom = percent_from_pagesize(height, bottom)
    return top, bottom


def percent_to_pagesize(
        size: float,
        percent: float,
) -> float:
    """Convert a percent value to page coordinates

    The top coordinate starts with 0.0 and ends on the bottom with 1.0.

    Args:
        size(float): paper height/width
        percent(float): [0.0; 1.0] of used size
    Returns:
        percentage page height/width value
    """
    assert size >= 0.0
    assert 0.0 <= percent <= 1.0

    result = (1.0 - percent) * size
    return result


def percent_from_pagesize(size, current) -> float:
    """Determine the percentage value of a pagesize

    Example:
        size    500
        current 100
        return  0.8%

    Hint:
        The max size start at the top of the page.

    Args:
        size(float): size of current page
        current(float):
    Returns:
        value in percent in range of [0.0, 1.0]
    """
    assert size > 0
    assert size >= current
    return current / size


def to_content(navigator: PageTextNavigator) -> TextBoundsList:
    result = list(navigator)
    return result


# Merge lines with lower distance to one text chunk.
MAX_MERGE_DISTANCE = 3.55  # TODO: Holy value
MAX_MERGE_HORIZONTALY = 14.0  # TODO: HOLY VALUE


def merge_content(
        text: TextBoundsList,
        max_x_merge=MAX_MERGE_HORIZONTALY,
        max_y_merge=MAX_MERGE_DISTANCE,
        uindex=None,
) -> TextBoundsList:
    """Merge content blocks to create greater content blocks depending on
    merge strategy.

    Args:
        text: chunk with BoundingBox to merge
        max_x_merge(float): feed distance between the two left sides
        max_y_merge(float): vertical distance between 2 BoundingBoxes to
                            merge them into one
        uindex(list[int]): undefined index to link text(TextBoundsList) with
                           text-source if uindex is None, the `uindex` is an
                           ascending list starting with zero.
    Returns:
        (result, merged) - result is the merged content, merged - stores the
                           uindex which are merged together
    """
    if not text:
        # Nothing to merge
        return []

    # ensure input
    for (_, item) in text:
        assert isinstance(item, str), str(item)

    uindex = list(range(len(text))) if uindex is None else uindex
    bounds = navigator_to_bounds(text)
    font_distance = fontdistance(bounds)
    feed_distance = feeddistance(bounds)

    # copy element
    result = [(text[0][0], [text[0][1]])]
    merged = [[uindex[0]]]
    lines = zip(font_distance, feed_distance)
    for index, (fontdist, feeddist) in enumerate(lines, start=1):
        current_bounds, current_text = text[index]
        if fontdist > max_y_merge:
            # new entree
            result.append((current_bounds, [current_text]))
            merged.append([uindex[index]])
            continue
        if abs(feeddist) > max_x_merge:
            # new entree
            result.append((current_bounds, [current_text]))
            merged.append([uindex[index]])
            continue

        # Merge me
        member_location, member_content = result[-1]
        merger_location, merger_content = text[index]
        member_content.append(merger_content)
        merged[-1].append(uindex[index])
        # merged items together and save them as last item
        result[-1] = (
            common_box([member_location, merger_location]),
            member_content,
        )

    return result, merged


def merge_content_join(result):
    result = [(bounds, NEWLINE.join(item)) for (bounds, item) in result]
    return result


def navigator_to_bounds(navigator: PageTextNavigator) -> List[BoundingBox]:
    """Extract list of `BoundingBox` from `PageTextNavigator`"""
    return [item for item, _ in navigator]
