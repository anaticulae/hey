# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import caption.serialize


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
    figures = caption.serialize.load_image_informations_fromfiles(
        figures,
        pages=pages,
    )

    processor = caption.feature.CaptionPageWordProcessor(
        words=(
            'Abb.',
            'Abbildung',
            'Fig.',
            'Figure',
        ))

    result = caption.feature.run(processor, ptcns, figures)

    dumped = caption.serialize.dump_captions(result)
    return dumped
