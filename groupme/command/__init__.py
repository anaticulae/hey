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

from groupme import __version__
from groupme.feature.chapter import chapter_to_yaml
from groupme.feature.chapter import chapters
from groupme.feature.toc import toc
from groupme.feature.toc import toc_to_yaml

PROCESS_NAME = 'groupme'


@saveme
def main():
    parser = create_parser(
        version=__version__,
        outputparameter=True,
        inputparameter=True,
        prog=PROCESS_NAME,
    )
    args = parse(parser)
    inputpath, outputpath = sources(args)
    textpath = check_resources(inputpath, outputpath, parser)
    try:

        document = load_document(file_read(textpath))
        tableofcontent = toc(document)
        toc_dumped = toc_to_yaml(tableofcontent)

        chapter = chapters(document)
        chapter_dumped = chapter_to_yaml(chapter)

        toc_output = join(outputpath, 'groupme__toc.yaml')
        chapter_output = join(outputpath, 'groupme__chapter.yaml')

        logging('write result to: %s' % outputpath)
        file_create(toc_output, toc_dumped)
        file_create(chapter_output, chapter_dumped)

        # Write content to file.
    except Exception as error:  #pylint: disable=broad-except
        logging_error(error)
        logging_stacktrace()
        return FAILURE
    return SUCCESS


def check_resources(inputpath: str, outputpath: str, parser):
    if not inputpath and not outputpath:
        parser.print_help()
        exit(FAILURE)

    textpath = join(inputpath, 'rawmaker__text_text.yaml')
    if not exists(textpath):
        logging_error('Missing text path %s' % textpath)
        exit(INVALID_COMMAND)
    return textpath
