# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""

Institution - Institut
Department - Fakultaet
Institute - Institut
Field - Fachgebiet
Course of studies - Studiengang
Academic year - Studienjahr/Semester
"""

from dataclasses import dataclass

from utila import NEWLINE
from utila import flatten


@dataclass
class Institution:
    courseofstudies: str = None
    department: str = None
    field: str = None
    institute: str = None
    university: str = None


def parse(raw: str) -> Institution:
    university = find_institution(raw)
    if university:
        university, raw = university

    results = []
    for item in [DEPARTMENT, INSTITUTE, FIELD, COURSES]:
        parsed, raw = detection(raw, item)
        if parsed:
            assert len(parsed) == 1, str(parsed)
            parsed = parsed[0]
        else:
            parsed = None
        results.append(parsed)

    (department, institute, field, courses) = results

    result = Institution(
        courseofstudies=courses,
        department=department,
        field=field,
        institute=institute,
        university=university,
    )
    return result, raw


def detection(raw, items, remove: bool = True):
    if isinstance(items, str):
        items = [items]
    # FIRST DRAFT

    splitted = raw.split(',')
    splitted = flatten([item.split(NEWLINE) for item in splitted])
    result = []
    for item in items:
        for chunk in splitted:
            if item in chunk:
                if remove:
                    # use words after `collector` as the result
                    prepared = chunk.split(item)[1].strip()
                    result.append(prepared)
                else:
                    result.append(chunk)
                raw.replace(chunk, '')

    # make results unique
    result = list(set(result))
    return result, raw


SELECTOR = {
    'Akademisch',
    'College',
    'Erlangung',
    'Fachbereich',
    'Fachgebiet',
    'Faktultät',
    'Grad',
    'Grades',
    'Hochschule',
    'Institut',
    'Studiengang',
    'Universität',
}


def words(raw):
    result = raw
    for item in [',', '.', '-', NEWLINE]:
        result = result.replace(item, ' ')
    result = result.split()
    result = [item.title() for item in result]
    return result


INSTITUTE = [
    'Institut',
]

DEPARTMENT = [
    'Faktultät',
]

FIELD = [
    'Fachgebiet',
    'Fachbereich',
]

UNIVERSITY = [
    'Hochschule',
    'Universität',
]

COURSES = ['Studiengang']

# TODO: Load from dictonary
UNIVERSITIES = [
    'Duale Hochschule Baden-Würtemberg',
    'Hochschule für Technik und Wirtschaft Berlin',
    'Technische Universität Berlin',
    'Technische Universität Darmstadt',
    'Universität Münster',
]


def find_institution(raw) -> str:
    """Check that `institution` is in UNIVERSITIES dictonary

    Args:
        institution(str):
    Returns:
        None if `institution` is in dictonary else collected
    """
    splitted = raw.split(',')
    splitted = flatten([item.split(NEWLINE) for item in splitted])
    # TODO require better lookup technology with hashing
    collected = [
        item for item in UNIVERSITIES
        if any([test for test in splitted if item in test])
    ]
    if not collected:
        return None, raw
    assert len(collected) == 1, 'More than one institution is collected'
    collected = collected[0]

    rest = raw.replace(collected, '')
    return collected, rest
