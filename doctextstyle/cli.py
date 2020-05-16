# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila
import utila.cli

import doctextstyle
import doctextstyle.extractor
import doctextstyle.serialize

DEFAULT_OUTPUT_FILE = 'docstyle__textstyle.yaml'


@utila.saveme
def main() -> int:
    commands = []
    parser = utila.cli.create_parser(
        todo=commands,
        config=utila.ParserConfiguration(
            outputparameter=True,
            inputparameter=True,
            prefix=False,
            pages=True,
        ),
        version=doctextstyle.__version__,
        prog=doctextstyle.PROCESS,
    )
    args = utila.parse(parser)
    selected_pages = pages_fromargs(args)

    inpath, outpath = utila.cli.sources(args, singleinput=True)
    inpath = inpath[0]

    if os.path.isdir(outpath):
        outpath = os.path.join(outpath, DEFAULT_OUTPUT_FILE)

    # ensure that output directory exists
    parent, _ = os.path.split(outpath)
    os.makedirs(parent, exist_ok=True)

    try:
        extracted = doctextstyle.extractor.extract(inpath, pages=selected_pages)
    except FileNotFoundError as error:
        utila.error('missing input location')
        utila.error(f'{error}')
        return utila.FAILURE

    dumped = doctextstyle.serialize.dump_docstyle(extracted)
    utila.file_replace(outpath, dumped)
    return utila.SUCCESS


def pages_fromargs(args) -> tuple:
    """Extract list of pages number out of user input args.

    >>> pages_fromargs({'pages':[0, 5,'10:15'], 'inpath':'...',})
    (0, 5, 10, 11, 12, 13, 14)
    """
    # TODO: REPLACE AFTER UTILA
    pages = args.get('pages', [':'])
    pages = [str(item) for item in pages]
    joined = ','.join(pages)
    result = utila.parse_pages(joined)  # pylint:disable=R0204
    return result
