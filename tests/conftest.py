# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import SUCCESS
from utila import run
from utila.test import LONGRUN
from utila.test import clean_install

from hey import ROOT
from tests.resources import TEST_DATA

pytest_plugins = 'pytester'  # pylint: disable=invalid-name

if LONGRUN:  # skip with --test=fast
    # install correct power version
    clean_install(ROOT, 'hey')

    completed = run('power --all', TEST_DATA)  # pylint:disable=C0103
    assert completed.returncode == SUCCESS, str(completed)
