# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Alternate TextLine Group
========================

Group items due analyse alternating line-text-feed changes.

We assume that we analyse only text-content. Therefore we can ignore
text which differs to much from standard text size.

Currently we compute the most 2 text feed groups. But in general we can
extend this algorithm to more `lining points`.

Requirements
------------

- oneline_text
- oneline_textpositions

-> OnelinePageTextNavigator

Example:

..code-block:: none

    RÖLL, Franz J. (1998): Mythen und Symbole in populären Medien. Der wahrnehmungs
             orientierte Ansatz in der Medienpädagogik. Frankfurt a. Main: GEP.

    RYSSEL, Dirk (2012): Dreiakter/Dreiaktstruktur. In: Lexikon der Filmbegriffe. Online
             verfügbar unter: http://filmlexikon.uni-kiel.de/index.php?
             action=lexikon&tag= det&id=2401 [Letzter Zugriff: 28.10.2014].

    SARBIN, Theodore R. (Hg.) (1986): Narrative Psychology. The Storied Nature
            of Human Conduct. New York: Praeger.

    SARBIN, Theodore R. (1986): Introduction and Overview. In: Sarbin 1986, ix-xviii.

    SCHENK, Michael (32007): Medienwirkungsforschung. Tübingen: Mohr Siebeck.
"""

import utila

import hey.classificator
import hey.textnavigator.fonts
import hey.textnavigator.multiline

MIN_LINE_ELEMENT = 3  # TODO: HOLY VALUE
MAX_LINE_DIFF = 10

MAX_TEXT_DIFF = 2.5


def parse_page(page) -> list:
    """Iterate through lines in document.

    A group is separated by an alternating text feed. We skip all
    elements which are not part of most common feed or not part of most
    common font size.

    A group is closed when:

        * the text feed is equal than first element in group
        * an illegal text feed occurs
        * an illegal font size

    Hint: Keep in mind when extending to more than one group, that one
    group can contain other groups.
    """
    if not page:
        return None
    starts = group_line_start(page)
    if not starts:
        utila.error('could not find any lining points')
        return None
    textsize = hey.textnavigator.fonts.textsize_from_page(page)
    result = []
    current = None
    for line in page:
        x0 = line.bounding[0]
        if not utila.near(textsize, line.style.textsize(), MAX_TEXT_DIFF):
            # illegal font size
            current = None
            continue
        if current is None:
            if not inside(starts, x0):
                # illegal line feed
                # seek to start position or next valid item
                continue
            result.append([line])
            current = x0
        else:
            if not inside(starts, x0):
                # illegal line feed
                current = None
                continue
            if utila.near(current, x0, diff=MAX_LINE_DIFF):
                # alternating position
                current = x0
                result.append([line])
            else:
                # member of group
                result[-1].append(line)
    return result


def inside(starts, value):
    return any((utila.near(item, value, MAX_LINE_DIFF) for item in starts))


def group_line_start(page):
    x0_pos = [item.bounding[0] for item in page]
    clusters = hey.classificator.max_distance(
        x0_pos,
        diff=MAX_LINE_DIFF,
        min_elements=MIN_LINE_ELEMENT,
    )
    if len(clusters) < 2:
        return None

    # from left to right
    items = [item.center for item in clusters[0:2]]
    first, second = min(items), max(items)
    return first, second
