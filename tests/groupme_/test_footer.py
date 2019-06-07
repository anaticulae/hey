"""
Extract footer out of document.
"""

from iamraw import Document
from pytest import fixture
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_pageborders

from groupme.feature.footer import load_textposition
from groupme.textnavigator import load_pagetextnavigator
from tests.groupme_ import SIMPLE_HORIZONTAL
from tests.groupme_ import SIMPLE_PAGESIZE
from tests.groupme_ import SIMPLE_POSITION
from tests.groupme_ import SIMPLE_TEXT


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

    navigator = load_pagetextnavigator(position, document)
    return navigator, horizontals


def test_simple_example(simple):
    navigator, horizontals = simple
    assert len(navigator) == len(horizontals)
