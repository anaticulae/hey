# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

from detector.parser import textblock_token
from detector.parser.date import parse as parse_date
from detector.parser.institution import parse as parse_institution
from detector.parser.matrikel import parse as parse_matrikel
from detector.parser.person import order_persons
from detector.parser.person import parse_all as parse_person_all
from detector.parser.thesis import parse as parse_thesis
from detector.parser.title import parse as parse_title
from hey.textnavigator.navigator import PageTextNavigator


def parse(text: PageTextNavigator) -> iamraw.TitlePage:
    """Extract `TitlePage` out of tile page data

    Args:
        text(PageTextNavigator/str): complete text content of title page
                                     with NEWLINES. Ordinary str input
                                     in conveted to PageTextNavigator
                                     with equal BoundingBoxes
    Returns:
        extracted TitlePage
    """
    assert isinstance(text, PageTextNavigator), type(text)
    result = iamraw.TitlePage()
    title = parse_title(text)

    text = utila.NEWLINE.join([item.text for item in text[:]])
    if isinstance(title, str):
        text.replace(title, '')
        result.title = title
    else:
        # TODO: check title error lstatus
        pass

    result.institution, text = parse_institution(text)
    parsed = textblock_token(text)

    undecided = []
    # run single/simple parsing tasks
    for (sink, action) in STRATEGY:
        for index, item in enumerate(parsed):
            collected = action(item)
            if collected:
                setattr(result, sink, collected)
                rest = item.replace(collected.raw, '').strip()
                if not rest:
                    parsed.remove(item)
                else:
                    # after replacement some data is left, try to use a further
                    parsed[index] = rest
                break
        else:
            undecided.append(action)

    # run complex parsing
    persons, todo = parse_person_all(parsed)
    if persons:
        result.author, result.examiner = order_persons(persons)

    return result


def valid_titlepage(titlepage: iamraw.TitlePage) -> bool:
    if titlepage is None:
        return False
    assert titlepage.title is None or titlepage.title.strip(
    ) == titlepage.title, f'invalid parsing result "{titlepage.title}"'
    if titlepage.title in ('Inhaltsverzeichnis', 'Inhalt', 'Content'):
        return False
    return True


STRATEGY = [
    ('date', parse_date),
    ('thesis', parse_thesis),
    ('matrikel', parse_matrikel),
]
