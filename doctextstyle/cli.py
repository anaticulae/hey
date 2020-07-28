# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import serializeraw
import utila
import utila.cli

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


@utila.saveme
def main() -> int:
    commands = []
    parser = utila.cli.create_parser(
        todo=commands,
        description=DESCRIPTION,
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
    selected_pages = utila.pages_fromargs(args)

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

    dumped = serializeraw.dump_doctextstyle(extracted)
    utila.file_replace(outpath, dumped)
    return utila.SUCCESS
