# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import serializeraw
import yaml

import groupme.border.leftright
import groupme.border.most


def work(
        sizeandborder: str,
        textpositions: str,
        pages: tuple = None,
) -> typing.Tuple[str]:
    sizeandborder = serializeraw.load_pageborders(sizeandborder, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)

    expected = determine_border(textpositions, sizeandborder)

    pages_loaded = sorted(
        list({item.page for item in sizeandborder} |
             {item.page for item in textpositions}))
    result = []
    for page in pages_loaded:
        result.append((page, expected(page)))

    dumped = yaml.dump(result)
    return dumped


def determine_border(
        textpositions: iamraw.PageContentTextPositions,
        pagesizes: iamraw.PageSizeBorderList,
):
    most = groupme.border.most.run(pagesizes)
    leftright = groupme.border.leftright.run(textpositions, pagesizes)

    def border_detector(page: int):
        # left, right, top, down
        # TODO: CHECK THAT PAGE CALL IS CORRECT
        left = leftright.left
        if isinstance(left, tuple):
            left = left[page % 2]  # pylint:disable=E1136

        right = leftright.right
        if isinstance(right, tuple):
            right = right[page % 2]  # pylint:disable=E1136

        result = (left, right, most.top, most.bottom)
        return result

    return border_detector
