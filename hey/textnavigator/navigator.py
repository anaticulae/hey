# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import List
from typing import Tuple

from iamraw import Border
from iamraw import BoundingBox
from iamraw import Document
from iamraw import PageSize
from utila import INF

from hey.textnavigator.fonts import TextBoundsList
from hey.textnavigator.fonts import fontdistance

START = 0.0
END = 1.0


class PageTextNavigator:
    """The direction of the text is top down and left to right"""

    def __init__(self, size=(612.0, 792.0)):
        self.data = []
        self.width, self.height = size

    def insert(self, box: BoundingBox, item: str):
        """Insert text element top to bottom and left to right

        Args:
            box(BoundingBox): position and dimension of text area
            item(str): content of text chunck
        """
        x0, y0, x1, y1 = box
        assert 0 <= x0 <= x1 <= self.width
        assert 0 <= y0 <= y1 <= self.height

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
        """Count text chuncks"""
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

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
        assert START <= top <= bottom <= END
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


class PageTextContentNavigator:

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
        msg = 'require `PageTextNavigator` got: %s'
        assert isinstance(textnavigator,
                          PageTextNavigator), msg % type(textnavigator)
        msg = 'require `Border` got: %s'
        assert isinstance(content, Border), msg % type(content)
        pagesize = PageSize(
            width=textnavigator.width,
            height=textnavigator.height,
        )
        top, bottom = topbottom(pagesize, content)
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
        text_position,
) -> PageTextNavigators:
    navigators = []
    for page, textposition in enumerate(text_position):
        navigator = PageTextNavigator()
        navigators.append(navigator)
        textid = 0
        for item in text[page]:
            try:
                # TODO: Remove strip after container is fixed
                content = item.text.strip()
                pos = textposition[textid]
                navigator.insert(pos, content)
                textid += 1
            except AttributeError:
                pass

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
        The maxsize start at the top of the page.

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
    # result = [(bounding, item) for bounding, item in navigator]
    result = list(navigator)
    return result


# Merge lines with lower distance to one text chunck.
MAX_MERGE_DISTANCE = 3.55  # TODO: Holy value


def merge_content(text: TextBoundsList) -> TextBoundsList:
    bounds = navigator_to_bounds(text)

    if not text:
        # Nothing to merge
        return []

    distance = fontdistance(bounds)
    result = []

    result.append(text[0])  # single item is always merged
    for index, dist in enumerate(distance, start=1):
        if dist > MAX_MERGE_DISTANCE:
            result.append(text[index])
            continue
        # Merge me
        (member_location), content = result[-1]
        (merger_location), c_content = text[index]

        content = '%s\n%s' % (content, c_content)
        # merged items together and save them as last item
        result[-1] = (
            common_box([member_location, merger_location]),
            content,
        )
    return result


def common_box(items) -> BoundingBox:
    """Determine largest box which contains the border of all `items`"""
    # TODO: replace with utila code
    x0, y0, x1, y1 = INF, INF, -INF, -INF
    for (cx0, cy0, cx1, cy1) in items:
        x0 = min(x0, cx0)
        y0 = min(y0, cy0)
        x1 = max(x1, cx1)
        y1 = max(y1, cy1)
    return BoundingBox.from_list([x0, y0, x1, y1])


def navigator_to_bounds(navigator: PageTextNavigator) -> List[BoundingBox]:
    """Extract list of `BoundingBox` from `PageTextNavigator`"""
    return [item for item, _ in navigator]
