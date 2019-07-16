# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from os.path import join

from utila import FAILURE
from utila import error
from utila import file_create
from utila import run

from tests.resources import RESOURCES
from tests.resources import TEST_DATA


def write_capsys(capsys):
    """Save logged capsys to filespace"""
    stdout, stderr = capsys.readouterr()
    file_create('logging.txt', stdout)
    file_create('error.txt', stderr)


def startup():
    """Check that required test resources exists and if not generate them.
    After generation, check resources again and fail if some does not exist.
    """
    missing = any([not exists(item) for item in RESOURCES])

    if not missing:
        return
    before = join(TEST_DATA, 'before.sh')
    completed = run('sh %s' % before)

    if completed.returncode:
        error(completed)
        exit(FAILURE)

    for item in RESOURCES:
        msg = 'missing resource: %s' % item
        assert exists(item), msg


startup()
