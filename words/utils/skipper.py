# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def should_skip(page: int, pages: tuple) -> bool:  # pylint:disable=W0621
    """Determine if `page` is invalid.

    If `pages` is None, every page is accepted.
    If `pages` is a list, only the elements in this list are valid and return
    False.

    Args:
        page(int): check to skip this page number
        pages(tuple): tuple with accepted pages, !require tuple to serialize!
    Returns:
        return True if `page` is in `pages` or pages is None else False
    """
    if pages is None:
        return False
    if not isinstance(pages, tuple):
        pages = (pages,)
    # support multiple pages
    if isinstance(page, tuple):
        # ensure that all (page..) are in range
        start, end = page
        return any([should_skip(pp, pages) for pp in range(start, end + 1)])
    return not page in pages
