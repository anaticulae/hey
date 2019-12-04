# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here"""

import random
import typing

import utila


def choose_random(items, count: int = 5) -> list:
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
    random.shuffle(items)
    return items[0:count]


def sync(iterators) -> typing.Tuple[int, typing.List]:
    """Generator to synchronize a list of PageContentIterators.

    Args:
        iterators(list): list of `PageContent`-Iterators
    Yields:
        pagenumber: (content of current pagenumber...)
    """
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
        # lowest page number of popped content
        pagenumber = min([page(item) for item in popped])

        deliver = [
            item if page(item) == pagenumber else None for item in popped
        ]
        yield pagenumber, tuple(deliver)

        for index, item in enumerate(popped):
            # push back non-yielded items
            if page(item) != pagenumber:
                # use as a stack, therefore push(append) and pop(pop), not
                # insert on pos 0.
                copy[index].append(item)


def page(item):
    if item is None:
        return utila.INF
    try:
        return item.page
    except AttributeError:
        return item.number


# Unicode special minus sign
SPECIAL_MINUS_SIGN = '–'
