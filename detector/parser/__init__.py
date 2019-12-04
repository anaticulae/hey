# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from re import Match

from utila import NEWLINE


# TODO: MOVE TO UTILA
def extract_match(matched):
    assert isinstance(matched, Match), type(matched)
    return matched.string[matched.span()[0]:matched.span()[1]]


def textblock_token(text: str):
    """Split textpage into connected textblocks which are separated by empty
    newlines.

    Args:
        text(str): text page with textchunks
    Returns:
        list of splitted chunks
    """
    if not text:
        return []
    splitted = text.splitlines()
    result = []
    current = []
    for item in splitted:
        if item:
            current.append(item)
        else:  # newline
            if current:
                result.append(NEWLINE.join(current))
                current = []
    if current:
        result.append(NEWLINE.join(current))
    return result
