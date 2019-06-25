#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import os

from hey import PACKAGE_NAME as HEY_PACKAGE_NAME
from hey import __version__ as HEY_VERSION

__version__ = HEY_VERSION

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS_NAME = 'groupme'
PACKAGE_NAME = HEY_PACKAGE_NAME
