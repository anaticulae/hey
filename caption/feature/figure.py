# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
# TODO: REMOVE FIGURE STEP
# OUTDATED
import serializeraw

import caption.feature.image
import caption.processor


def work(
    text_oneline: str,
    textposition_oneline: str,
    sizeandborder: str,
    footerheader: str,
    *figures: list,
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
    figures = serializeraw.load_image_infos_fromfiles(
        figures,
        pages=pages,
        skip_hidden=True,
    )
    processor = caption.processor.CaptionPageWordProcessor(
        words=CAPTIONS,
        typ=iamraw.CaptionType.FIGURE,
    )
    # determine result
    result = caption.processor.run(processor, ptcns, figures)
    # dump
    dumped = serializeraw.dump_captions(result)
    return dumped


CAPTIONS = caption.feature.image.CAPTIONS
