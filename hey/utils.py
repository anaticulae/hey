# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here"""

from os import makedirs
from os.path import join

from utila import FAILURE
from utila import saveme
from utila.cmdline import parse
from utila.feature import commandline
from utila.feature import create_parser
from utila.feature import find_features
from utila.feature import process
from utila.feature import read_workplan
from utila.feature import sources


@saveme(systemexit=True)
def featurepack(
        workplan,
        root: str,
        feature_package: str,
        name: str,
        description: str,
        version: str,
):
    feature_path = join(root, feature_package.replace('.', '/'))
    feature = find_features(feature_path, feature_package)
    commands = commandline(feature)
    parser = create_parser(
        commands,
        prog=name,
        description=description,
        version=version,
        outputparameter=True,
        inputparameter=True,
    )
    args = parse(parser)

    # evaluate the verbose flag
    inputpath, outputpath, verbose = sources(args, verbose=True)
    if not inputpath or not outputpath:
        parser.print_usage()
        return FAILURE

    workplan = read_workplan(workplan, inputpath, outputpath, verify=True)

    # Ensure to have output folder
    makedirs(outputpath, exist_ok=True)

    completed = process(workplan, verbose=verbose)
    return completed
