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

from detector.parser import textblock_token
from detector.parser.date import TitleDate
from detector.parser.date import parse as parse_date
from detector.parser.matrikel import Matrikel
from detector.parser.matrikel import parse as parse_matrikel
from detector.parser.person import Person
from detector.parser.person import order_persons
from detector.parser.person import parse_all as parse_person_all
from detector.parser.thesis import DocumentType
from detector.parser.thesis import parse as parse_thesis


@dataclass
class TitlePage:
    title: str = ''
    thesis: DocumentType = None
    date: TitleDate = None
    author: Person = None
    matrikel: Matrikel = None
    examiner: List[Person] = field(default_factory=list)


def parse(text: str) -> TitlePage:
    """Extract `TitlePage` out of tile page data

    Args:
        text(str): complete text content of title page with NEWLINES
    Returns:
        extracted TitlePage
    """
    parsed = textblock_token(text)

    undecided = []
    result = TitlePage()

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
