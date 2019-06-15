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


class PageTextNavigator:
    """The direction of the text is top down and left to right"""

    def __init__(self, size=(612.0, 792.0)):
        self.data = []
        self.width, self.height = size

    def __getitem__(self, index):
        return self.data[index]

    def insert(self, box: BoundingBox, item):
        x_bottom, y_bottom, x_top, y_top = box

        insert_position = 0
        for pos, _ in self.data:
            if int(pos.y_top) == int(y_top):
                if int(x_bottom) <= int(pos.x_bottom):
                    break
            elif y_top >= pos.y_top:
                break
            insert_position += 1
        self.data.insert(insert_position, (box, item))

    def __len__(self):
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
            List[PageObjects]
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

    def between(self, top, bottom):
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
):
    # height(float[0.0,1.0]): 0.0 is top, 1.0 is bottom
    assert size >= 0.0
    assert 0.0 <= percent <= 1.0

    result = (1.0 - percent) * size
    return result


def percent_from_pagesize(size, current):
    """
    size    500
    current 100
    return  0.8%
    """
    assert size > 0
    assert size >= current

    return (size - current) / size
