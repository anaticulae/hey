# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def parses(raw: str):
    """\
    >>> parses('Becker, W.; Ulrich, P.; Botzkowski, T.; Eurich, S.')
    [['Becker', 'W.'], ['Ulrich', 'P.'], ['Botzkowski', 'T.'], ['Eurich', 'S.']]
    >>> parses('AASLID, R. - BRUBAKK, AO.')
    [['AASLID', 'R.'], ['BRUBAKK', 'AO.']]
    >>> parses('Beirness, D. and Vogel-Sprott, M.')
    [['Beirness', 'D.'], ['Vogel-Sprott', 'M.']]
    """
    free = freeand(raw)
    semicolon = simple(raw)
    hyphen = simple(raw, extern='-', intern=',')

    result = [free, semicolon, hyphen]
    balanced = [balance(item) for item in result]
    max_balance = maxindex(balanced)
    return result[max_balance]


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


def balance(authors):
    if not authors:
        return None
    common = [valid_author(author) for author in authors]
    valid = len([item for item in common if item])
    ratio = valid / len(common)
    return ratio


def valid_author(author):
    if len(author) != 2:
        return False
    for item in author:
        if ';' in item:
            return False
        if ',' in item:
            return False
    return True


def maxindex(items):
    if not items:
        return None
    current = 0
    for index, value in enumerate(items[1:], start=1):
        if value > items[current]:
            current = index
    return current
