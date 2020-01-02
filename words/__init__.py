# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The word package is a text processor which convert the pdf file into a
text markup for further analysis.

The package supports the following features:

    Chapter:            with title and number
    Font:               bold, italic, underline
    Hyperlinks:
    List:               sorted, unsorted
    Text:               headlines(h1,h2,h3...), sentences(.,?,!,:)

Required resources: text, font, position

"""
import os

from hey import PACKAGE as HEY_PACKAGE
from hey import __version__ as HEY_VERSION

__version__ = HEY_VERSION

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'words'
PACKAGE = HEY_PACKAGE

HEADLINE_STEP = 'headlines'
HEADLINE_STEP_RESULT = 'headlines'
HEADLINES = f'{HEADLINE_STEP}_{HEADLINE_STEP_RESULT}'

WORDS_HEADLINES = f'{PROCESS}__{HEADLINES}.yaml'
