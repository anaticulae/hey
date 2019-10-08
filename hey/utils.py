# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here"""

from random import shuffle

from utila import INF


def choose_random(items, count: int = 5):
    """Chose `count` random items of a collection

    Hint:
        This process does not change the source collection. There are no side
        effects.
    Args:
        items(list): data collection to select random items
        count(int): number of items to retun
    Returns:
        `count` selected items out of collections
      """

    items = list(items)  # create a copy
    shuffle(items)
    return items[0:count]


def sync(iterators):
    # TODO: NOT GOOD, BUT WORKS
    # reverse list to use as a stack with push and pop
    copy = [list(reversed(list(item))) for item in iterators]

    while copy:
        popped = []
        # iterate over all iterators and pop the first element
        for item in copy:
            try:
                popped.append(item.pop())
            except IndexError:
                popped.append(None)
        if not any(popped):
            # nothing to do anymore
            return
        minimum = min([page(item) for item in popped])
        deliver = [item if page(item) == minimum else None for item in popped]
        yield minimum, tuple(deliver)

        for index, item in enumerate(popped):
            if page(item) != minimum:
                copy[index].append(item)


def page(item):
    if item is None:
        return INF
    try:
        return item.page
    except AttributeError:
        return item.number


# Unicode special minus sign
SPECIAL_MINUS_SIGN = '–'


def select_content(item, default):
    try:
        return item.content
    except AttributeError:
        return default
