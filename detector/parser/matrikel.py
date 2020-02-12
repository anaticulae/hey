# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The module is able to parse "Matrikel" numbers out of the title page of a
thesis paper.

Matrikel numbers can have different formats:

    Matrikelnummer: 519448
    Matrikel-Nr. 1024577
    vorgelegt von: 321240
    16348
    ...

There are two parts, the intro, which leads to the number e.g.
`Matrikelnummer:` and the number itself like 321240. Some title pages does
not contains a matrikel-number-intro.

"""

import re

import iamraw
import utila


def parse(raw: str) -> iamraw.Matrikel:
    """Parse matrikel number from text line

    Args:
        raw(str): raw text of title page
    Returns:
        parsed `Matrikel` or None if nothing matched
    """
    raw = raw.strip()
    result = re.search(PATTERN, raw)
    if not result:
        return None
    intro = result['intro']
    number = int(result['number'])
    raw = utila.extract_match(result).strip()  # TODO: remove after fixing regex
    matrikel = iamraw.Matrikel(number=number, intro=intro, raw=raw)
    return matrikel


INTRO = [
    '',
    r'Matrikel-Nr\.',
    'Matrikelnummer',
    'vorgelegt von',
]

PATTERN = r'(?P<intro>(' + '|'.join(INTRO) + r')?[:,]?)\s?'
PATTERN += r'(?P<number>\d{4,10})'  # number contains from 4 to 10 digits
