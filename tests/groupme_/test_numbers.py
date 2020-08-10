# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Extract footer out of document."""

import typing

import iamraw.path
import power
import pytest
import serializeraw
import utila
import utilatest

import groupme.feature.numbers
# pylint:disable=W0611
from tests.fixtures.restruct import restructured_pagetextnavigators
from tests.fixtures.simple import simple
from tests.fixtures.simple import simple_navigator


def test_simple_example(simple):  #pylint:disable=W0621
    navigator, horizontals = simple
    assert len(horizontals) == 1  # first page contains horizontals
    assert len(navigator) == 7


def test_footer_simple(simple):  #pylint:disable=W0621
    navigator, _ = simple
    result = groupme.feature.numbers.footer(navigator)

    # cluster with page numbers
    assert len(result) == 1


def test_header_simple(simple):  #pylint:disable=W0621
    navigator, _ = simple
    result = groupme.feature.numbers.header(navigator)
    assert not result


def test_footer_restructured(restructured_pagetextnavigators):  #pylint:disable=W0621
    result = groupme.feature.numbers.footer(
        restructured_pagetextnavigators,
        numbers_only=False,
    )
    # cluster with page numbers
    # 2 Pages and some header text lines
    assert len(result) == 3, utila.log_raw(result)


def test_header_restructured(restructured_pagetextnavigators):  #pylint:disable=W0621
    result = groupme.feature.numbers.header(restructured_pagetextnavigators)
    # Example:
    # (5,
    # (BoundingBox(x_bottom=72.00, y_bottom=746.33, x_top=336.99, y_top=758.84),
    # 'The RestructuredText Book Documentation, Release 0.1'))

    # 2 lines of header, one for the left and one for the right page/side
    assert len(result) == 2, utila.log_raw(result)


def test_pagenumbers_restructured(restructured_pagetextnavigators):  #pylint:disable=W0621
    result = groupme.feature.numbers.footer(restructured_pagetextnavigators)

    numbers = groupme.feature.numbers.pagenumbers(result)

    # left and right page
    assert len(numbers) == 2

    # need number in left and/or right page
    assert sum([len(number) for number in numbers])

    left = [item[2] for item in numbers[0]]
    right = [item[2] for item in numbers[1]]

    expected_left = ['ii', 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
    expected_right = ['i', 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

    assert left == expected_left
    assert right == expected_right


def test_pagenumbers_simple(simple_navigator):  #pylint:disable=W0621
    result = groupme.feature.numbers.footer(simple_navigator)

    # single page
    numbers = groupme.feature.numbers.pagenumbers(result)

    assert isinstance(numbers, typing.Iterable), numbers
    assert numbers


@pytest.fixture
def pagenumbers_simple(simple_navigator):  #pylint:disable=W0621
    result = groupme.feature.numbers.footer(simple_navigator)
    # single page
    numbers = groupme.feature.numbers.pagenumbers(result)

    assert isinstance(numbers, typing.Iterable), numbers
    assert numbers
    return numbers


@pytest.mark.parametrize('resource, expected_numbers', [
    pytest.param(power.link(power.BACHELOR111_PDF), 16, id='bachelor111'),
    pytest.param(power.link(power.MASTER072_PDF), 69, id='master72pages'),
    pytest.param(power.link(power.TECHNICAL_024), 23, id='technical24pages'),
])
@utilatest.skip_longrun
def test_groupme_numbers_work_single(resource, expected_numbers):
    # TODO: bottom only, add header page extraction
    text = iamraw.path.text(resource)
    text_positions = iamraw.path.textposition(resource)

    result = groupme.feature.numbers.work(text, text_positions)
    result = serializeraw.load_pagenumbers(result)

    assert isinstance(result, list), f'wrong page detection type {type(result)}'
    assert len(result) == expected_numbers


@pytest.mark.parametrize('nopagenumber', ['', 'a'])
def test_groumpe_numbers_is_pagenumber_negative(nopagenumber):
    assert not groupme.feature.numbers.is_pagenumber(nopagenumber)


@pytest.mark.parametrize('pagenumber', ['xxc', '10'])
def test_groumpe_numbers_is_pagenumber(pagenumber):
    assert groupme.feature.numbers.is_pagenumber(pagenumber)


def test_numbers_restructured_without_title():
    """Ensure to extract correct pdf page on document which starts with
    empty page. Before this patch, the pdfpages started with zero
    instead of one."""
    source = power.link(power.DOCU27_PDF, folder='notitle')
    navigator = serializeraw.create_pagetextnavigators_frompath(source)
    pagenumbers = groupme.feature.numbers.determine_pagenumbers(navigator)
    pagenumbers = utila.flatten(pagenumbers)  # pylint:disable=R0204
    pagenumbers = sorted(pagenumbers, key=lambda x: x[0])
    expected_pdfpages = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    current = [item[0] for item in pagenumbers]
    assert current == expected_pdfpages, str(current)
