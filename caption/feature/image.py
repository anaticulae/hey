# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila

import caption.processor


def work(
    text_oneline: str,
    textposition_oneline: str,
    sizeandborder: str,
    footerheader: str,
    *images: list,
    pages: tuple = None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text_oneline,
        textposition_oneline,
        sizeandborderpath=sizeandborder,
        headerfooterpath=footerheader,
        pages=pages,
    )
    # skip hidden: do not determine caption for images which are part of a
    # figure.
    images = serializeraw.load_image_infos_fromfiles(
        images,
        pages=pages,
        skip_hidden=True,
    )
    # setup
    processor = caption.processor.CaptionPageWordProcessor(
        words=CAPTIONS,
        typ=iamraw.CaptionType.FIGURE,
    )
    # run
    result = caption.processor.run(processor, ptcns, images)
    dumped = serializeraw.dump_captions(result)
    return dumped


# TODO: Introduce special mechanism to dump them as tables
# Tab. Tabelle, Table to detect tables which are stored as image

CAPTIONS = utila.compiles(r"""
    ^
    (
        Abb\.|
        Abbildung|
        Fig\.|
        Figure|
        Foto|
        Tab\.|
        Tabelle|
        Table
    )
    [ ]{0,3}
    (
        (\d{1,2}|[A-Z])(\.\d{1,2})?
    )
    \:?
""")
