#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from utila import SUCCESS
from utila import Command
from utila import create_parser
from utila import logging_error
from utila import parse
from utila import saveme
from utila import sources

from hey import __version__


@saveme
def main():
    logging_error('No implemented')
    # parser = create_parser(
    #     version=__version__,
    #     outputparameter=True,
    #     inputparameter=True,
    # )
    # args = parse(parser)
    # inputpath, outputpath = sources(args)

    return SUCCESS
