# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import serializeraw
import utila

import caption.processor


def work(
    oneline_text: str,
    oneline_textposition: str,
    sizeandborder: str,
    footerheader: str,
    tables: str,
    pages: tuple = None,
) -> str:
    if not os.path.exists(tables):
        utila.error(f'could not load tables: {tables}, skip caption --table')
        # dump empty captions
        return serializeraw.dump_captions([])
    # prepare data
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        oneline_text,
        oneline_textposition,
        sizeandborderpath=sizeandborder,
        headerfooterpath=footerheader,
        pages=pages,
    )
    tables = serializeraw.load_tables(tables, pages=pages)
    # determien captions
    processor = caption.processor.CaptionPageWordProcessor(
        words=CAPTIONS,
        typ=iamraw.CaptionType.TABLE,
    )
    result = caption.processor.run(processor, ptcns, tables)
    # dump result
    dumped = serializeraw.dump_captions(result)
    return dumped


CAPTIONS = utila.compiles(r"""
    ^
    (
        Tab\.|
        Tabelle|
        Table|
        Abb\.|                  # Mark wrong used label? See HOME50p32
        Abbildung|
        Fig\.|
        Figure
    )
    [ ]{0,3}
    (
        (\d{1,2}|[A-Z])(\.\d{1,2})?
    )
    \:?
""")
