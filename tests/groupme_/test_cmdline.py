# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila.test import run
from utila.test import skip_not_virtual

from groupme import ROOT


@skip_not_virtual
def test_run_groupme():
    """Install groupme and run groupme --help to ensure basic function"""
    uninstall = 'pip uninstall hey -y'
    install = 'python setup.py install && groupme --help'

    clean_and_run = uninstall + ' && ' + install
    completed = run(clean_and_run, cwd=ROOT)
    assert completed.returncode == 0, completed.stdout + completed.stderr
