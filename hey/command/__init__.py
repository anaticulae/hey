#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from utila import SUCCESS
from utila import create_parser
from utila import parse
from utila import saveme
from utila import sources

from hey import __version__

COMMANDS = [] # add additonal commands here

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

    return SUCCESS
