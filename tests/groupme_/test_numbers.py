"""
Extract footer out of document.
"""

from typing import Iterable

from pytest import fixture

from groupme.feature.numbers import footer
from groupme.feature.numbers import header
from groupme.feature.numbers import pagenumbers
# pylint:disable=W0611
from tests.fixtures.restruct import restructured
from tests.fixtures.restruct import restructured_navigator
from tests.fixtures.simple import simple
from tests.fixtures.simple import simple_navigator


def test_simple_example(simple):  #pylint:disable=W0621
    navigator, horizontals = simple
    assert len(navigator) == len(horizontals)


def test_footer_simple(simple):  #pylint:disable=W0621
    navigator, _ = simple
    result = footer(navigator)

    # cluster with page numbers
    assert len(result) == 1


def test_header_simple(simple):  #pylint:disable=W0621
    navigator, _ = simple
    result = header(navigator)
    assert not result


def test_footer_restructured(restructured_navigator):  #pylint:disable=W0621
    result = footer(restructured_navigator)

    # cluster with page numbers
    # 2 Pages and some header text lines
    assert len(result) == 5, print_cluster(result)


def test_header_restructured(restructured_navigator):  #pylint:disable=W0621
    result = header(restructured_navigator)
    # Example:
    # (5,
    # (BoundingBox(x_bottom=72.00, y_bottom=746.33, x_top=336.99, y_top=758.84),
    # 'The RestructuredText Book Documentation, Release 0.1'))

    # 2 lines of header, one for the left and one for the right page/side
    assert len(result) == 2, print_cluster(result)


def test_pagenumbers_restructured(restructured_navigator):  #pylint:disable=W0621
    result = footer(restructured_navigator)

    numbers = pagenumbers(result)

    # left and right page
    assert len(numbers) == 2

    # need number in left and/or right page
    assert sum([len(number) for number in numbers])


def test_pagenumbers_simple(simple_navigator):  #pylint:disable=W0621
    result = footer(simple_navigator)

    # single page
    numbers = pagenumbers(result)

    assert isinstance(numbers, Iterable), numbers
    assert numbers


@fixture
def pagenumbers_simple(simple_navigator):  #pylint:disable=W0621
    result = footer(simple_navigator)
    # single page
    numbers = pagenumbers(result)

    assert isinstance(numbers, Iterable), numbers
    assert numbers
    return numbers


@fixture
def pagenumbers_restructured(restructured_navigator):  #pylint:disable=W0621
    result = footer(restructured_navigator)
    # double page
    left, right = pagenumbers(result)
    return left, right


def print_cluster(clusters):
    for cluster in clusters:
        print()
        for item in cluster:
            print(item)
