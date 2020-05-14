# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

PageTextProperties = collections.namedtuple(
    'PageTextProperties',
    'length, sizes, fonts, distances',
)
PageTextPropertiesList = typing.List[PageTextProperties]

TextProperty = collections.namedtuple(
    'TextProperty',
    'length, size, font, before, after, ypos',
)
TextProperties = typing.List[TextProperty]
