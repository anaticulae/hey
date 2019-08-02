# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from glob import glob
from os.path import exists
from os.path import join

from utila import FAILURE
from utila import error
from utila import file_create
from utila import run

from tests.resources import TEST_DATA


def write_capsys(capsys):
    """Save logged capsys to filespace"""
    stdout, stderr = capsys.readouterr()
    file_create('logging.txt', stdout)
    file_create('error.txt', stderr)


def pdfs():
    """Collect all pdf files in test folder"""
    pattern = join(TEST_DATA, '**/*.pdf')
    located = glob(pattern, recursive=True)
    return located
