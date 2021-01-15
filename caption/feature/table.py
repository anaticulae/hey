# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import caption.feature


def work(
        oneline_text: str,
        oneline_textposition: str,
        sizeandborder: str,
        footerheader: str,
        tables: str,
        pages: tuple = None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        oneline_text,
        oneline_textposition,
        sizeandborderpath=sizeandborder,
        headerfooterpath=footerheader,
        pages=pages,
    )
    tables = serializeraw.load_tables(tables, pages=pages)

    processor = caption.feature.CaptionPageWordProcessor(
        words=(
            'Tab.',
            'Tabelle',
            'Table',
        ))

    result = caption.feature.run(processor, ptcns, tables)
    dumped = serializeraw.dump_captions(result)
    return dumped
