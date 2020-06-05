# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BibRefTechParser
================

Parses technical bibliographic reference like:

.. code-block:: none

    [WL11]
    [Rum05, Seite 10]

"""

import contextlib
import re

import utila

import detector.bibliography.data

# [ ]{0,3} Optional whitespaces

TECHNICAL = r"""\[[ ]{0,3}
                (?P<author>[\w\.]{2,3}[+]{0,1})[ ]{0,3}
                (?P<year>\d{2})[ ]{0,3}
                (?P<number>a|b|c|d){0,1}[ ]{0,3}
                (\,[ ]{0,3}Seite[ ]{0,3}
                (
                 (?P<page>\d{1,3})|
                 (?P<pagestart>\d{1,3})[ ]{0,3}\-[ ]{0,3}(?P<pageend>\d{1,3})
                )
                ){0,1}
                [ ]{0,3}\]
             """


def parses(content: str) -> detector.bibliography.data.BibliographyReferences:
    result = []
    for item in re.finditer(TECHNICAL, content, re.VERBOSE):
        raw = utila.extract_match(item)
        page, pageend = None, None
        with contextlib.suppress(KeyError, TypeError):
            page = int(item['page'])
        with contextlib.suppress(KeyError, TypeError):
            page, pageend = int(item['pagestart']), int(item['pageend'])
        number = item['number'] if item['number'] else None

        reference = detector.bibliography.data.BibliographyReference(
            page=page,
            pageend=pageend,
            reference=item['author'],
            year=item['year'],
            number=number,
            raw=raw,
        )
        result.append(reference)
    return result
