# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BibRef AND(&) Parser
====================

.. code-block:: none

    Schmidt, R., Dettmeyer, R., Padosch, S. & Madea, B. (2000b). A
    review of the literature on the Effects of Low Doses of Alcohol on
    driving-Related Skills. National Highway Traffic Safety
    Administration (NHTS), Southern California Research Institute,
    Washington.

Authors
-------

Correct
~~~~~~~

* Schmidt, R., Dettmeyer, R., Padosch, S. & Madea, B.

Failures
~~~~~~~~

* Schnabel, Eva
* Sdao-Jarvie, K. and Vogel-Sprott, M.

"""

import re

import iamraw

import detector.bibliography.reference.authors as dbra

AND = r"""
    (?P<authors>.+)
    \(
        (?P<year>\d{4})
        (?P<number>a|b|c|d){0,1}  # optional char
    \)
    [ ]{0,5}                      # remove trailing whitespaces
    \.{0,1}                       # remove dot
    [ ]{0,5}                      # remove trailing whitespaces
    (?P<content>.+)
"""


def parse_longtext(content: str) -> iamraw.BibliographyReference:
    content = content.replace('\n', ' ')
    matched = re.search(AND, content, re.VERBOSE)
    if not matched:
        return None

    authors = dbra.freeand(matched['authors'])
    year = int(matched['year'])
    number = matched['number'] if matched['number'] else None

    try:
        title, rest = matched['content'].split('.', maxsplit=1)  # pylint:disable=W0612
    except ValueError:
        title, rest = None, matched['content']

    result = iamraw.BibliographyReference(
        authors=authors,
        number=number,
        title=title,
        year=year,
        raw=content,
    )
    return result
