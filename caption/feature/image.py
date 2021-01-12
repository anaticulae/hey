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
import caption.serialize

# TODO: Introduce special mechanism to dump them as tables
# Tab. Tabelle, Table to detect tables which are stored as image
KEYWORDS = (
    'Abb.',
    'Abbildung',
    'Fig.',
    'Figure',
    'Foto',
    'Tab.',
    'Tabelle',
    'Table',
)


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
    images = caption.serialize.load_image_informations_fromfiles(
        images,
        pages=pages,
    )

    processor = caption.feature.CaptionPageWordProcessor(words=KEYWORDS)

    result = caption.feature.run(processor, ptcns, images)
    dumped = serializeraw.dump_captions(result)
    return dumped
