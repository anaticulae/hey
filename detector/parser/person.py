# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from collections import namedtuple
from enum import Flag
from enum import auto
from operator import attrgetter
from re import search

from detector.parser import extract_match

Person = namedtuple('Person', 'title name firstname raw')


def parse(raw: str) -> Person:
    """Parse `Person` out of name line

    Args:
        raw(str):
    Returns
        Person if parsing was successful, else None
    """
    result = search(PATTERN, raw)
    if not result:
        return None

    title = extract_title(result)
    title = merge_title(title)

    name, firstname = result['name'], result['fname']
    raw = extract_match(result)
    person = Person(title=title, name=name, firstname=firstname, raw=raw)
    return person


def parse_all(items):
    """Parse title content to extract a list of Persons

    Args:
        items(str): content of title page
    Returns:
        detected list of Persons and the rest of the page content as a list
    """
    persons = []
    rest = []
    for item in items:
        lines = item.splitlines()
        for line in lines:
            parsed = parse(line)
            if not parsed:
                rest.append(line)
                continue
            rest.append(line.replace(parsed.raw, ''))
            persons.append(parsed)
    return persons, rest


def order_persons(persons):
    """Sort persons by academical rank and return the lowester rang as author
    and the rest as examier.

    Args:
        persons(list[Person]):
    Returns:
        author(Person), examines as a list of persons
    """
    if not persons:
        return None
    # sort persons by title and name as a tiebraker
    persons = sorted(persons, key=attrgetter('title', 'name'))
    author, examiner = persons[0], persons[1:]
    return author, examiner


class Title(Flag):
    NONE = auto()
    BSC = auto()
    MASTER = auto()
    DR = auto()
    PROF = auto()

    def __lt__(self, item):
        # make `Title` orderable
        try:
            return self.value < item.value  # pylint:disable=comparison-with-callable
        except ValueError:
            return False

    @staticmethod
    def fromstring(value):
        try:
            return MATCHES[value]
        except KeyError:
            return None

    @staticmethod
    def keys():
        return [item for item in MATCHES]


MATCHES = {
    'B.Sc.': Title.BSC,
    'Dipl. Ing.': Title.MASTER,
    'Dr.': Title.DR,
    'Dr.-Ing.': Title.DR,
    'M.Sc.': Title.MASTER,
    'Prof.': Title.PROF,
}

EXAMINER = [
    # it's important to limit parsing length to avoid very long running parsing
    r'Erstgutachter',
    r'Zweitgutachter',
    r'Gutachter',
    r'Hochschullehrer',
    r'(\d\.\s?)?Betreuer',
    r'(\w+\s?){1,4}',
]

PREPHASE = r'(?P<examiner>(' + '|'.join(EXAMINER) + r')[:]?\s?)?'
PATTERN = '|'.join('(?P<t%d>%s)' % (index, item.replace('.', r'\.'))
                   for index, item in enumerate(Title.keys()))
PATTERN = r'(%s\ *)+( )?(?P<fname>(\w+[ ]?)*) (?P<name>\w+)' % PATTERN
PATTERN = PREPHASE + PATTERN


def extract_title(result):
    title = []
    for item in range(len(Title.keys())):
        try:
            parsed_title = result['t%d' % item]
            if not parsed_title:
                continue
        except KeyError:
            continue
        else:
            title.append(Title.fromstring(parsed_title))
    return title


def merge_title(items) -> Title:
    if not items:
        return None
    result = items[0]
    for item in items:
        result |= item
    return result
