# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""There are two types of person which must appear on the titlepage. The
author and examiner. An author can have an academic title. An Examiner
must have an academic title.

Examples:

    Author:
        Vorgelegt von Helmut Konrad Fahrendholz

    Examiner:
        Prof. Dr. Nobert Bolz
        Zweitgutachter: Dipl.-Medienberater Stephan Frühwirt
"""
import enum
import operator
import re

import iamraw

import detector.parser


def parse(raw: str) -> iamraw.Person:
    """Parse `Person` out of name line

    Args:
        raw(str):
    Returns
        Person if parsing was successful, else None
    """
    result = re.search(PATTERN, raw)
    if not result:
        # try second parser
        result = parse_person_without_title(raw)
        if result:
            return result
        return None
    title = extract_title(result)
    title = merge_title(title)

    name, firstname = result['name'], result['fname']
    raw = detector.parser.extract_match(result)
    person = iamraw.Person(title=title, name=name, firstname=firstname, raw=raw)
    return person


def parse_person_without_title(raw: str) -> iamraw.Person:
    """Parse `Person`s without any academic title. In general, this is
    the author of the document.

    Hint:
        Examiner must have an academic title, but in some thesis this is not
        so. Therefore we have to mark it later as an error.
    """
    raw = raw.strip()

    preamble = [
        r'vorgelegt von',
        r'Erstprüfer',  # TODO: Remove this later
        r'Zweitprüfer',
    ]
    preamble = '(' + '|'.join(
        fr'(?P<t{index}>{item})' for index, item in enumerate(preamble)) + ')'
    between = r'[:]?[ ]{0,8}'
    name = r'(?P<names>(\w+\s{0,5}){1,5})'

    pattern = re.compile(preamble + between + name, re.IGNORECASE)
    matched = re.search(pattern, raw)
    if not matched:
        return None
    firstname, name = matched['names'].rsplit(' ', maxsplit=1)
    firstname, name = firstname.strip(), name.strip()

    title = author_or_examiner(raw)

    result = iamraw.Person(
        title=title,
        name=name,
        firstname=firstname,
        raw=detector.parser.extract_match(matched),
    )
    return result


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
    persons = sorted(persons, key=operator.attrgetter('title', 'name'))
    author, examiner = persons[0], persons[1:]
    return author, examiner


class Title(enum.Flag):
    # TODO: MOVE TO IAMRAW
    NO_TITLE = enum.auto()
    STUDENT = enum.auto()  # author without academic title
    BSC = enum.auto()
    MASTER = enum.auto()
    EXAMINIER = enum.auto()  # examiner without academic title
    DR = enum.auto()
    PROF = enum.auto()

    def __lt__(self, item):
        # make `Title` orderable
        try:
            return self.value < item.value  # pylint:disable=comparison-with-callable
        except ValueError:
            return False
        except AttributeError:
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


PROF_DR = Title.PROF | Title.DR

MATCHES = {
    'B.Sc.': Title.BSC,
    r'Dipl.-\w+': Title.MASTER,
    'Dipl. Ing.': Title.MASTER,
    'M.A.': Title.MASTER,
    'M.Sc.': Title.MASTER,
    'Dr.-Ing.': Title.DR,
    'Dr.': Title.DR,
    'Prof.': Title.PROF,
    r'\w+. ': Title.DR,
    # see general pattern above
    # 'Dr. rer. biol. hum.': Title.DR,
    # 'Dr. med.': Title.DR,
}

EXAMINER = [
    # it's important to limit parsing length to avoid very long running parsing
    r'(\d\.\s?)?Betreuer',
    r'Erstgutachter',
    r'Gutachter',
    r'Hochschullehrer',
    r'Zweitgutachter',
    # [\s|:] to avoid confusing 'Prof. Dr. Theo Wil'
    r'(\w+\s?){1,4}?[\s|:]',
    r'^',
]

TITLE_KEYS = [
    item.replace('.', r'\.').replace(' ', '[ ]')
    for item in Title.keys()
    if item
]
MATCHER = '|'.join(
    fr'(?P<t{index}>{item})[\ ]?' for index, item in enumerate(TITLE_KEYS))
EXAMINER = '|'.join(EXAMINER)

PATTERN = rf"""(?P<examiner>({EXAMINER})[:]?\s?)?
               ({MATCHER}\ *)+(\ )?
               (?P<fname>(\w+[ ]?)*)\ (?P<name>[\w|-]+)
            """
PATTERN = re.compile(PATTERN, re.X)


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
            matches = [item for item in MATCHES.values()]
            title.append(matches[item])
    return title


def author_or_examiner(raw: str) -> Title:
    raw = raw.lower()

    author = ['vorgelegt']
    if any([item in raw for item in author]):
        return Title.STUDENT

    examiner = ['prüfer', 'gutachter']
    if any([item in raw for item in examiner]):
        return Title.EXAMINIER

    return Title.NO_TITLE


def merge_title(items) -> Title:
    if not items:
        return None
    result = items[0]
    for item in items:
        if not item:
            continue
        result |= item
    return result
