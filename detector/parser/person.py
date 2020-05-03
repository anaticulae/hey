# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Titlepage: Person Parser
========================

There are two types of person which must appear on the titlepage. The
author and examiner. An author can have an academic title. An Examiner
must have an academic title.

Examples:

    Author:
        Vorgelegt von Helmut Konrad Fahrendholz

    Examiner:
        Prof. Dr. Nobert Bolz
        Zweitgutachter: Dipl.-Medienberater Stephan Frühwirt
"""
import operator
import re
import typing

import iamraw
import iamraw.person
import utila


def parse(raw: str) -> iamraw.Person:
    """Parse `Person` out of name line

    Args:
        raw(str): raw parsing text
    Returns:
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
    raw = utila.extract_match(result)
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
    # TODO: Keep attention to the list below. Refactor later
    preamble = [
        r'Erstprüfer(in)?',  # TODO: Remove this later
        r'Autor(in)?',
        r'Verfasser(in)?',
        r'Zweitprüfer(in)?',
        r'vorgelegt von',
    ]
    preamble = [fr'(?P<t{index}>{item})' for index, item in enumerate(preamble)]
    preamble = '(' + '|'.join(preamble) + ')'  # pylint:disable=R0204
    between = r'[:]?[\s ]{0,8}'
    name = r'(?P<names>(\w+[ ]{0,5}){1,5})\b'
    pattern = re.compile(preamble + between + name, re.IGNORECASE)

    matched = re.search(pattern, raw)
    if not matched:
        return None
    try:
        # TODO: SUPPORT SINGLE NAME?
        # TODO: LINT TO VERIFY PRE AND SUR NAME
        firstname, name = matched['names'].rsplit(' ', maxsplit=1)
    except ValueError:
        utila.error(f'could not split: {matched["names"]}; {matched}')
        return None
    firstname, name = firstname.strip(), name.strip()

    title = author_or_examiner(raw)
    result = iamraw.Person(
        title=title,
        name=name,
        firstname=firstname,
        raw=utila.extract_match(matched),
    )
    return result


def parse_all(items: list) -> list:
    """Parse title content to extract a list of Persons.

    Args:
        items(list): content of title page
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
                # check area to parse more than one line
                area = lookbehind(rest)
                if area is not None:
                    persons.append(area[0])
                    rest = area[1]
                    continue
                continue
            rest.append(line.replace(parsed.raw, ''))
            persons.append(parsed)
    return persons, rest


def lookbehind(rest):
    complete = '\n'.join(rest)
    parsed = parse(complete)
    if not parsed:
        return None
    complete = complete.replace(parsed.raw, '')
    rest = [item for item in complete.splitlines() if item.strip()]
    return parsed, rest


# TODO: REPLACE AFTER UPGRADING IAMRAW
iamraw.Persons = typing.List[iamraw.Person]


def order_persons(persons: list) -> typing.Tuple[iamraw.Person, iamraw.Persons]:
    """Sort persons by academical rank and return the lowester rang as author
    and the rest as examier.

    Args:
        persons(list[Person]): list to order
    Returns:
        author(Person), examines as a list of persons
    """
    if not persons:
        return None
    # sort persons by title and name as a tiebraker
    persons = sorted(persons, key=operator.attrgetter('title', 'name'))

    if any([
            persons[0].title in (iamraw.AcademicTitle.EXAMINIER,
                                 iamraw.AcademicTitle.DR,
                                 iamraw.AcademicTitle.PROF),
            author_or_examiner(persons[0].raw) == iamraw.AcademicTitle.EXAMINIER
    ]):
        # author was not detected
        return None, persons

    author, examiner = persons[0], persons[1:]
    return author, examiner


EXAMINER = [
    # it's important to limit parsing length to avoid very long running parsing
    r'(\d\.\s?)?Betreuer(in)?',
    r'Erstgutachter(in)?',
    r'Gutachter(in)?',
    r'Hochschullehrer(in)?',
    r'Zweitgutachter(in)?',
    # [\s|:] to avoid confusing 'Prof. Dr. Theo Wil'
    r'(\w+\s?){1,4}?[\s|:]',
    r'^',
]

TITLE_KEYS = [
    item.replace('.', r'\.').replace(' ', '[ ]')
    for item in iamraw.AcademicTitle.keys()
    if item
]
PERSON_TITLE = '|'.join(
    fr'(?P<t{index}>{item})[\ ]?' for index, item in enumerate(TITLE_KEYS))
EXAMINER = '|'.join(EXAMINER)  # pylint:disable=R0204

PERSON_NAME = r'(?P<fname>(\w+[ ]?)*)\ (?P<name>[\w|-]+)'

PATTERN = rf"""(?P<examiner>({EXAMINER})[:]?\s?)?
               ({PERSON_TITLE}\ *)+(\ )?{PERSON_NAME}
            """
PATTERN = re.compile(PATTERN, re.X)


def extract_title(result):
    title = []
    for item in range(len(iamraw.AcademicTitle.keys())):
        try:
            parsed_title = result['t%d' % item]
            if not parsed_title:
                continue
        except KeyError:
            continue
        else:
            matches = [item for item in iamraw.person.MATCHES.values()]
            title.append(matches[item])
    return title


def author_or_examiner(raw: str) -> iamraw.AcademicTitle:
    raw = raw.lower()

    # Hint: add items as lower case
    author = ['vorgelegt', 'verfasser', 'autor']
    if any([item in raw for item in author]):
        return iamraw.AcademicTitle.STUDENT

    examiner = ['prüfer', 'gutachter', 'betreuer']
    if any([item in raw for item in examiner]):
        return iamraw.AcademicTitle.EXAMINIER

    return iamraw.AcademicTitle.NO_TITLE


def merge_title(items) -> iamraw.AcademicTitle:
    if not items:
        return None
    result = items[0]
    for item in items:
        if not item:
            continue
        result |= item
    return result
