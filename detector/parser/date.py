# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Parses dates from the first page of a thesis.

TODO:
    Make parser more tolerant, if nothing matches, reduces accuracy due
    reduce the search pattern like Januar -> Janua, Janu, .. Jan..

    Refactor and think about new concept
"""

import calendar
import functools
import re

import iamraw
import utila


def parse(raw: str) -> iamraw.TitleDate:
    """Convert `raw` line to `TitleDate`

    Args:
        raw(str): extracted line of pdf document
    Returns:
        return parsed TitleDate - return None if parsing is not possible
    """

    # Require different regex
    # Judge function to decide when having multiple results
    simple_alpha_date_month_first = functools.partial(
        simple_alpha_date,
        month=MONTH_ENG,
        pattern=SIMPLE_ALPHA_DATE_MONTH_FIRST,
    )

    pattern = [
        location_comma_day_month_year,
        simple_alpha_date,
        simple_alpha_date_month_first,
        simple_month_year_date,
        simple_date,
        semester_year,
    ] + [
        functools.partial(simple_alpha_date, reduce=index) for index in range(7)
    ]

    parsed = [parser(raw) for parser in pattern]
    parsed = [item for item in parsed if item]  # remove non matches
    # use longest matching pattern
    parsed = sorted(parsed, key=lambda x: len(x.raw), reverse=True)
    if not parsed:
        return None
    return parsed[0]


def validate_date(year, month, day):
    try:
        calendar.weekday(year, month, day)
    except ValueError:
        return False
    return True


MONTH = [
    'Januar',
    'Februar',
    'März',
    'April',
    'Mai',
    'Juni',
    'Juli',
    'August',
    'September',
    'Oktober',
    'November',
    'Dezember',
]

# TODO: Add shorten month name, see `Sep`

MONTH_ENG = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'Sep',
    'October',
    'November',
    'December',
]

MONTH_GROUP = r'(?P<month>' + '|'.join(MONTH) + ')'
MONTH_GROUP_ENG = r'(?P<month>' + '|'.join(MONTH_ENG) + ')'

SIMPLE_DATE = r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})'

SIMPLE_ALPHA_DATE = r'(?P<day>\d{1,2})([\.|,]) ' + MONTH_GROUP\
                                                 + r' (?P<year>\d{4})'
SIMPLE_ALPHA_DATE_MONTH_FIRST = MONTH_GROUP_ENG +   r' (?P<day>\d{1,2})([\.|,])'\
                                                 + r' (?P<year>\d{4})'

SIMPLE_MONTH_YEAR = MONTH_GROUP + r' (\d{4})'

LOCATION_COMMA_DAY_MONTH_YEAR = r'(?P<location>\w+), (den ){0,1}('\
                                                      + SIMPLE_ALPHA_DATE + ')'


def simple_date(raw):
    res = re.search(SIMPLE_DATE, raw)
    if not res:
        return None
    res = res.groups()
    valid = len(res[0]) == len(res[1]) == 2
    raw = '%s.%s.%s' % res
    year, month, day = int(res[2]), int(res[1]), int(res[0])
    result = iamraw.TitleDate(
        year=year,
        month=month,
        day=day,
        location=None,
        valid=valid,
        raw=raw,
    )
    return result


def reduce_word(word, count):
    reduced = word[0:len(word) - count]  # TODO: improve this
    if len(reduced) <= 3:
        return word[0:3]
    return reduced


def simple_alpha_date(  # pylint:disable=R0914
        raw,
        reduce: int = 0,
        month=None,
        pattern=SIMPLE_ALPHA_DATE,
):
    if not month:
        month = MONTH
    month_match = {reduce_word(item, reduce): item for item in month}
    changed_pattern = str(pattern)
    for key, value in month_match.items():
        changed_pattern = changed_pattern.replace(value, key)
    res = re.search(changed_pattern, raw)
    if not res:
        return None

    matched = utila.extract_match(res)
    day = int(res['day'])
    collected = month_match[res['month']]
    month_ = month.index(collected) + 1
    year = int(res['year'])
    valid = len(res['day']) == 2
    result = iamraw.TitleDate(
        year=year,
        month=month_,
        day=day,
        location=None,
        valid=valid,
        raw=matched,
    )
    return result


def simple_month_year_date(raw):
    res = re.search(SIMPLE_MONTH_YEAR, raw)
    if not res:
        return None
    res = res.groups()
    raw = '%s %s' % res
    month = MONTH.index(res[0]) + 1
    year = int(res[1])
    result = iamraw.TitleDate(
        year=year,
        month=month,
        day=None,
        location=None,
        valid=True,
        raw=raw,
    )
    return result


def location_comma_day_month_year(raw: str) -> iamraw.TitleDate:
    res = re.search(LOCATION_COMMA_DAY_MONTH_YEAR, raw)
    if not res:
        return None
    location = res['location']
    day = int(res['day'])
    month = MONTH.index(res['month']) + 1
    year = int(res['year'])
    valid = validate_date(year, month, day)

    raw = utila.extract_match(res)
    result = iamraw.TitleDate(
        year=year,
        month=month,
        day=day,
        location=location,
        valid=valid,
        raw=raw,
    )
    return result


SEMESTER = r'(Sommersemester|Wintersemester)[ ](?P<year>\d{4})'


def semester_year(raw: str) -> iamraw.TitleDate:
    """Parses year from semester text.

    >>> semester_year('BACHELORARBEIT von Martina Feilke Sommersemester 2009 SOLAR II').year
    2009
    """
    res = re.search(SEMESTER, raw)
    if not res:
        return None
    year = int(res['year'])
    result = iamraw.TitleDate(
        year=year,
        month=None,
        day=None,
        location=None,
        valid=True,
        raw=utila.extract_match(res),
    )
    return result
