# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import dataclasses
import os
import typing

import hey

__version__ = hey.__version__

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'doctextstyle'

PageTextProperties = collections.namedtuple(
    'PageTextProperties',
    'length, hashed, sizes, fonts, distances, ypos',
)
PageTextPropertiesList = typing.List[PageTextProperties]

TextProperty = collections.namedtuple(
    'TextProperty',
    'length, hashed, size, font, before, after, top, bottom',
)
TextProperties = typing.List[TextProperty]


@dataclasses.dataclass
class DocTextStyle:
    text_size: float = None
    text_distance: float = None
    text_family: int = None

    h1_size: float = None
    h1_before: float = None
    h1_after: float = None
    h1_family: int = None

    h2_size: float = None
    h2_before: float = None
    h2_after: float = None
    h2_family: int = None

    h3_size: float = None
    h3_before: float = None
    h3_after: float = None
    h3_family: int = None

    pagenumber_size: float = None
    pagenumber_family: int = None

    footnote_size: float = None
    footnote_distance: float = None
    footnote_family: int = None

    list_size: float = None
    list_before: float = None  # distance to text
    list_distance: float = None  # distance in list items
    list_after: float = None  # distance to text
    list_family: int = None
