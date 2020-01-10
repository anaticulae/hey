# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from glob import glob
from os.path import exists
from os.path import join

from utila import FAILURE
from utila import NEWLINE
from utila import error
from utila import file_create
from utila import forward_slash
from utila import run

from tests.resources import RESOURCES


def write_capsys(capsys):
    """Save logged capsys to filespace"""
    stdout, stderr = capsys.readouterr()
    file_create('logging.txt', stdout)
    file_create('error.txt', stderr)


def pdfs():
    """Collect all pdf files in test folder"""
    pattern = join(RESOURCES, '**/*.pdf')
    located = glob(pattern, recursive=True)
    return located


def relative_path(item):
    item = item.replace(RESOURCES, '')
    start_with_slash = item[0] in ('/', '\\')
    if start_with_slash:
        item = item[1:]

    item = forward_slash(item, save_newline=False)
    return item


def prepare(item):
    return item.replace(NEWLINE, '').replace(' ', '_')[0:40]
