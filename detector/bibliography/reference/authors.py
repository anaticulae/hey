# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def simple(raw: str, extern: str = ';', intern: str = ','):
    """\
    >>> simple('Becker, W.; Ulrich, P.')
    [['Becker', 'W.'], ['Ulrich', 'P.']]
    """
    result = []
    for item in raw.split(extern):
        result.append([it.strip() for it in item.split(intern)])
    return result


def freeand(raw: str):
    """\
    >>> freeand('Beirness, D. & Vogel-Sprott, M.')
    [['Beirness', 'D.'], ['Vogel-Sprott', 'M.']]
    """
    extracted = []
    try:
        # TODO: SOLVE `AND` PROBLEM ON OTHER PLACE?
        left, right = raw.split(' and ') if ' and ' in raw else raw.split('&')
        extracted.extend(left.split(','))
        extracted.extend(right.split(','))
    except ValueError:
        extracted.extend(raw.split(','))
    if not extracted:
        return None
    result = [[extracted[0]]]
    for item in extracted[1:]:
        item = item.strip()
        if len(result[-1]) == 1:
            result[-1].append(item)
        else:
            result.append([item])
    return result
