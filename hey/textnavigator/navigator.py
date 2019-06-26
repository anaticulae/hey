# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import List

from iamraw import BoundingBox
from iamraw import Document
from utila import INF

from hey.textnavigator import navigator_to_bounds
from hey.textnavigator.fonts import TextBoundsList
from hey.textnavigator.fonts import fontdistance


class PageTextNavigator:
    """The direction of the text is top down and left to right"""

    def __init__(self, size=(612.0, 792.0)):
        self.data = []
        self.width, self.height = size

    def __getitem__(self, index):
        return self.data[index]

    def insert(self, box: BoundingBox, item: str):
        """Insert text element top to bottom and left to right

        Args:
            box(BoundingBox): position and dimension of text area
            item(str): content of text chunck
        """
        x_bottom, y_bottom, x_top, y_top = box
        assert 0 <= x_bottom <= x_top <= self.width
        assert 0 <= y_bottom <= y_top <= self.height

        insert_position = 0
        for pos, _ in self.data:
            if int(pos.y_top) == int(y_top):
                if int(x_bottom) <= int(pos.x_bottom):
                    break
            elif y_top >= pos.y_top:
                break
            insert_position += 1
        self.data.insert(insert_position, (box, item))

    def __len__(self) -> int:
        """Count text chuncks"""
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def after(self, height, width=0.0):
        assert 0.0 <= height <= 1.0
        assert 0.0 <= width <= 1.0

        after = (1.0 - height) * self.height
        result = []
        for box, item in self.data:
            if box.y_top <= after:
                result.append((
                    box,
                    item,
                ))
        return result

    def before(self, height: float, width=0.0):
        """
        Args:
            height(float[0.0,1.0]): 0.0 is top, 1.0 is bottom
        Returns:
            List[(position, PageObjects)]
        """
        assert 0.0 <= height <= 1.0
        assert 0.0 <= width <= 1.0

        before = (1.0 - height) * self.height  # greater than
        result = []
        for box, item in self.data:
            if box.y_bottom >= before:
                result.append((
                    box,
                    item,
                ))
        return result

    def between(self, top: float, bottom: float):
        """Return the content between top(0.0) and bottom(1.0) position.

        Args:
            top(float):
            bottom(float):
        Returns:
            List[(position, content)]
        """
        assert 0.0 <= top <= bottom <= 1.0

        after = (1.0 - top) * self.height
        before = (1.0 - bottom) * self.height  # greater than
        result = []
        for box, item in self.data:
            # before and after are pixel coordinates
            if before <= box.y_top <= after:
                result.append((box, item))
        return result


def create_pagetextnavigator(
        position,
        document: Document,
) -> List[PageTextNavigator]:
    navigators = []
    for page, textposition in enumerate(position):
        navigator = PageTextNavigator()
        navigators.append(navigator)
        textid = 0
        for item in document[page]:
            try:
                # TODO: Remove strip after container is fixed
                content = item.text.strip()
                pos = textposition[textid]
                navigator.insert(pos, content)
                textid += 1
            except AttributeError:
                pass

    return navigators


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

    value = (size - current) / size
    assert 0.0 <= value < 1.0
    return value


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
