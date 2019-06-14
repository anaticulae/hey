#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from os import makedirs
from os.path import exists
from os.path import join

from serializeraw import load_document
from utila import FAILURE
from utila import INVALID_COMMAND
from utila import SUCCESS
from utila import Command
from utila import create_parser
from utila import create_step
from utila import featurepack
from utila import file_append
from utila import file_create
from utila import file_read
from utila import logging
from utila import logging_error
from utila import logging_stacktrace
from utila import parse
from utila import saveme
from utila import sources
from yaml import dump_all

from groupme import ROOT
from groupme import __version__
from groupme.feature.chapter import chapter_to_yaml
from groupme.feature.chapter import chapters
from groupme.feature.chapter import work as extract_chapter
from groupme.feature.numbers import work as extract_pagenumbers
from groupme.feature.toc import work as extract_toc

PROCESS_NAME = 'groupme'
DESCRIPTION = 'TODO'
WORKPLAN = [
    create_step(
        PROCESS_NAME,
        extract_chapter,
        inputs=[
            ('rawmaker', 'text_text'),
        ],
        output=('chapter',),
    ),
    create_step(
        PROCESS_NAME,
        extract_toc,
        inputs=[
            ('rawmaker', 'text_text'),
        ],
        output=('toc',),
    ),
    create_step(
        PROCESS_NAME,
        extract_pagenumbers,
        inputs=[
            ('rawmaker', 'text_text'),
            ('rawmaker', 'text_positions'),
        ],
        output=('pagenumbers',),
    )
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        feature_package='groupme.feature',
        name=PROCESS_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
