# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import utila


def validate(items: list):
    """Validate list of pageable items. If some `page` attribute is
    duplicated, raise ValueError.

    Args:
        items(list): list of objects with <page,content>
    Raises:
        ValueError: if some page attribute is duplicated.
    """
    # TODO: REMOVE AFTER UPGRADING IAMRAW
    counter = collections.Counter()
    for item in items:
        counter[item.page] += 1
    msg = []
    for page, value in counter.most_common():
        if value <= 1:
            continue
        msg.append(f'duplicated page: {page} ({value})')
    if msg:
        raise ValueError(utila.NEWLINE.join(msg))


class RectangleCheck:

    def __init__(self, max_diff: float = 0.0):
        self.max_diff = max_diff
        self.content = []

    def extend(self, x0, y0, x1, y1):
        self.content.append((x0, y0, x1, y1))

    def contains(self, x0, y0, x1, y1) -> bool:
        diff = self.max_diff / 2
        for x00, y00, x11, y11 in self.content:
            if all(((x00 - diff) <= x0 <= x1 <= (x11 + diff),
                    (y00 - diff) <= y0 <= y1 <= (y11 + diff))):
                return True
        return False

    def shrinken(self):
        """Reduce checking rectangles to minimal required. Remove
        rectangle is there are included in a parent rectangle."""
        self.content = utila.rectangle_merge(self.content)

    def __getitem__(self, index):
        return self.content[index]

    def __len__(self):
        return len(self.content)
