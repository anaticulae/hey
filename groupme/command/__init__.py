#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from os import makedirs
from os.path import join

from utila import FAILURE
from utila import SUCCESS
from utila import Command
from utila import create_parser
from utila import file_append
from utila import file_create
from utila import logging
from utila import logging_error
from utila import logging_stacktrace
from utila import parse
from utila import saveme
from utila import sources
from yaml import dump_all

from groupme import __version__
from groupme.feature.chapter import chapter
from groupme.feature.chapter import chapter_to_yaml
from groupme.feature.chapter import toc_to_yaml

NEW_DOC = '---'

COMMANDS = [
    Command(
        shortcut='-c',
        longcut='--compression',
        message='Write output to one file'),
]  # add additonal commands here


@saveme
def main():
    parser = create_parser(
        COMMANDS,
        version=__version__,
        outputparameter=True,
        inputparameter=True,
    )
    args = parse(parser)
    inputpath, output = sources(args)

    if not inputpath and not output:
        parser.print_help()
        exit(FAILURE)
    compression = args['compression']

    write_to_stdout = not output
    try:
        tableofcontent, chapters, _ = chapter(inputpath)
        tableofcontent = toc_to_yaml(tableofcontent)
        chapters = chapter_to_yaml(chapters)

        if write_to_stdout:
            logging(tableofcontent)
            logging('---')
            logging(chapters)
        else:
            makedirs(output, exist_ok=True)
            logging('write result to: %s' % output)
            if not compression:
                feature_toc = join(output, 'toc.yaml')
                feature_chapter = join(output, 'chapter.yaml')
                file_append(feature_toc, tableofcontent, create=True)
                file_append(feature_chapter, chapters, create=True)
            else:
                feature = join(output, 'output.yaml')
                yaml = '%s\n%s\n%s' % (tableofcontent, NEW_DOC, chapters)
                file_create(feature, yaml)

            # Write content to file.
    except Exception as error:
        logging_error(error)
        logging_stacktrace()
        return FAILURE
    return SUCCESS
