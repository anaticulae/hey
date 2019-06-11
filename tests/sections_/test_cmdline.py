# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import install_and_run
from utila.test import skip_nonvirtual

from sections import PACKAGE_NAME
from sections import PROCESS_NAME
from sections import ROOT


@skip_nonvirtual
def test_run_sections():
    """Install groupme and run groupme --help to ensure basic function"""
    install_and_run(ROOT, PACKAGE_NAME, PROCESS_NAME)
