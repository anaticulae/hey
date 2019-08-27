# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from dataclasses import dataclass
from dataclasses import field
from typing import List

from utila import NEWLINE

from detector.parser import textblock_token
from detector.parser.date import TitleDate
from detector.parser.date import parse as parse_date
from detector.parser.institution import Institution
from detector.parser.institution import parse as parse_institution
from detector.parser.matrikel import Matrikel
from detector.parser.matrikel import parse as parse_matrikel
from detector.parser.person import Person
from detector.parser.person import order_persons
from detector.parser.person import parse_all as parse_person_all
from detector.parser.thesis import DocumentType
from detector.parser.thesis import parse as parse_thesis
from detector.parser.title import parse as parse_title
from hey.textnavigator.navigator import PageTextNavigator


@dataclass
class TitlePage:
    title: str = ''
    thesis: DocumentType = None
    date: TitleDate = None
    author: Person = None
    matrikel: Matrikel = None
    examiner: List[Person] = field(default_factory=list)
    institution: Institution = None


def parse(navigator: PageTextNavigator) -> TitlePage:
    """Extract `TitlePage` out of tile page data

    Args:
        text(str): complete text content of title page with NEWLINES
    Returns:
        extracted TitlePage
    """
    result = TitlePage()
    if isinstance(navigator, PageTextNavigator):
        title = parse_title(navigator)
        text = NEWLINE.join(navigator)
        if isinstance(text, str):
            text.replace(title, '')
            result.title = title
        else:
            # TODO: check title error lstatus
            pass
    else:
        # TODO: Legacy interface
        # support str as input
        text = navigator

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
    result.author, result.examiner = order_persons(persons)
    return result


STRATEGY = [
    ('date', parse_date),
    ('thesis', parse_thesis),
    ('matrikel', parse_matrikel),
]
