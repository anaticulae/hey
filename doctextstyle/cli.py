# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import serializeraw
import utilo
import utilo.cli

import doctextstyle
import doctextstyle.extractor

DEFAULT_OUTPUT_FILE = 'doctextstyle__textstyle.yaml'

DESCRIPTION = """\
Extracts common text layout properties for text, headlines(h1, h2, h3),
pagenumber, footnotes, paragraphs and lists.

Requires: `rawmaker__oneline` data to create pagetextnavigators
          `rawmaker__oneline` data to create pagecontenttextnavigators

Writes: `doctextstyle__textstyle.yaml`
"""


@utilo.saveme
def main() -> int:
    commands = []
    parser = utilo.cli.create_parser(
        todo=commands,
        description=DESCRIPTION,
        config=utilo.ParserConfiguration(
            inputparameter=True,
            multiprocessed=True,
            outputparameter=True,
            pages=True,
            prefix=False,
        ),
        version=doctextstyle.__version__,
        prog=doctextstyle.PROCESS,
    )
    args = utilo.parse(parser)
    utilo.log('run doctextstyle')
    selected_pages = utilo.pages_fromargs(args)

    inpath, outpath = utilo.cli.sources(args, singleinput=True)  # pylint:disable=W0632
    inpath = inpath[0]

    if os.path.isdir(outpath):
        outpath = os.path.join(outpath, DEFAULT_OUTPUT_FILE)

    # ensure that output directory exists
    parent, _ = os.path.split(outpath)
    os.makedirs(parent, exist_ok=True)

    try:
        extracted = doctextstyle.extractor.extract(inpath, pages=selected_pages)
    except FileNotFoundError as error:
        utilo.error('missing input location')
        utilo.error(f'{error}')
        return utilo.FAILURE

    dumped = serializeraw.dump_doctextstyle(extracted)
    utilo.file_replace(outpath, dumped)
    utilo.log('completed')
    return utilo.SUCCESS
