"""
Extract footer out of document.
"""

from typing import Iterable

from iamraw import Document
from pytest import fixture
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_pageborders

from groupme.feature.numbers import dump_pagenumbers
from groupme.feature.numbers import footer
from groupme.feature.numbers import header
from groupme.feature.numbers import load_pagenumbers
from groupme.feature.numbers import load_textposition
from groupme.feature.numbers import pagenumbers
from hey.textnavigator.navigator import create_pagetextnavigator
from tests.resources import RESTRUCT_HORIZONTAL
from tests.resources import RESTRUCT_PAGESIZE
from tests.resources import RESTRUCT_TEXT
from tests.resources import RESTRUCT_TEXT_POSITION
from tests.resources import SIMPLE_HORIZONTAL
from tests.resources import SIMPLE_PAGESIZE
from tests.resources import SIMPLE_POSITION
from tests.resources import SIMPLE_TEXT


# TODO: Remove after upgrading `iamraw`
def __len__(self):
    return len(self.pages)


Document.__len__ = __len__


@fixture
def simple():
    pagesize = load_pageborders(SIMPLE_PAGESIZE)
    horizontals = load_horizontals(SIMPLE_HORIZONTAL)
    position = load_textposition(SIMPLE_POSITION)
    document = load_document(SIMPLE_TEXT)

    assert pagesize
    assert horizontals
    assert position

    assert len(position) == len(document)
    assert len(horizontals) == len(document)

    navigator = create_pagetextnavigator(position, document)
    return navigator, horizontals


@fixture
def simple_navigator(simple):  #pylint:disable=W0621
    navigator, _ = simple
    return navigator


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


@fixture
def restructured():
    pagesize = load_pageborders(RESTRUCT_PAGESIZE)
    horizontals = load_horizontals(RESTRUCT_HORIZONTAL)
    position = load_textposition(RESTRUCT_TEXT_POSITION)
    document = load_document(RESTRUCT_TEXT)

    assert pagesize
    assert horizontals
    assert position

    assert len(position) == len(document)
    assert len(horizontals) == len(document)

    navigators = create_pagetextnavigator(position, document)
    return navigators, horizontals


@fixture
def restructured_navigator(restructured):  #pylint:disable=W0621
    navigators, _ = restructured
    return navigators


@fixture
def restructured_sizeandborder():
    size, border = load_pageborders(RESTRUCT_PAGESIZE)
    return size, border


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


def test_dump_and_load_pagenumbers_simple(pagenumbers_simple):  #pylint:disable=W0621
    dumped = dump_pagenumbers(pagenumbers_simple)
    assert len(dumped) > 100

    loaded = load_pagenumbers(dumped)
    assert loaded == pagenumbers_simple


def test_dump_and_load_pagenumbers_restructured(pagenumbers_restructured):  #pylint:disable=W0621
    dumped = dump_pagenumbers(pagenumbers_restructured)
    assert len(dumped) > 100

    loaded = load_pagenumbers(dumped)
    assert loaded == pagenumbers_restructured


def print_cluster(clusters):
    for cluster in clusters:
        print()
        for item in cluster:
            print(item)
