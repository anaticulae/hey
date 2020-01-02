#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""
* Introduction
    * Titlepage
    * Thank you
    * Copyright etc.
    * Erklaerung
* Table-Area
    * Table of content
    * Short cuts
    * Figure table
* Content
    * Chapter
        * Figure
        * Text
        * Headlines
* Table-Area-B
* Appendix
    * Resources
    * Link
    * Literature
"""

import os

from hey import PACKAGE as HEY_PACKAGE
from hey import __version__ as HEY_VERSION

__version__ = HEY_VERSION

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'sections'
PACKAGE = HEY_PACKAGE
