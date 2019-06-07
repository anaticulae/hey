"""
Start working on footer extractor.

Required resources:

    # PageSize
    # HorizontalLines
    # Text annotated with location

Required API:

    # before/ after method to determine items
"""

from iamraw import BoundingBox
from serializeraw import load_pageborders
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import load


def work():
    pass


def determine_footer(pagesizes, textlocations, horizontals):
    top, bottom = [], []

    return top, bottom
    # size, border = load_pageborders


def load_textposition(content: str):
    # TODO: This is from rawmaker->position.py,
    # TODO: remove after moving to serialzeraw
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    result = []
    for page in loaded:
        pagedata = {}
        for item in page['content']:
            key, position = item.split(maxsplit=1)
            pagedata[int(key)] = BoundingBox.from_str(position)
        result.append(pagedata)
    return result
