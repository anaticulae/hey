# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Extract footer out of document.
"""
import typing

import pytest

import groupme.feature.numbers
# pylint:disable=W0611
from tests.fixtures.restruct import restructured
from tests.fixtures.restruct import restructured_navigator
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


@pytest.mark.fail(reason='new implementation removes non numeric numbers')
def test_footer_restructured(restructured_navigator):  #pylint:disable=W0621
    result = groupme.feature.numbers.footer(restructured_navigator)

    # cluster with page numbers
    # 2 Pages and some header text lines
    assert len(result) == 5, print_cluster(result)


def test_header_restructured(restructured_navigator):  #pylint:disable=W0621
    result = groupme.feature.numbers.header(restructured_navigator)
    # Example:
    # (5,
    # (BoundingBox(x_bottom=72.00, y_bottom=746.33, x_top=336.99, y_top=758.84),
    # 'The RestructuredText Book Documentation, Release 0.1'))

    # 2 lines of header, one for the left and one for the right page/side
    assert len(result) == 2, print_cluster(result)


def test_pagenumbers_restructured(restructured_navigator):  #pylint:disable=W0621
    result = groupme.feature.numbers.footer(restructured_navigator)

    numbers = groupme.feature.numbers.pagenumbers(result)

    # left and right page
    assert len(numbers) == 2

    # need number in left and/or right page
    assert sum([len(number) for number in numbers])


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


@pytest.fixture
def pagenumbers_restructured(restructured_navigator):  #pylint:disable=W0621
    result = groupme.feature.numbers.footer(restructured_navigator)
    # double page
    left, right = groupme.feature.numbers.pagenumbers(result)
    return left, right


def print_cluster(clusters):
    for cluster in clusters:
        print()
        for item in cluster:
            print(item)
