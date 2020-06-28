# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import texmex
import utila

import caption.data
import caption.serialize
import caption.utils


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

    result = []
    for page in ptcns:
        pageimages = utila.select_page(images, page.page)
        pageimages = caption.utils.sorted_bounds(pageimages)
        processed = process_page(page, pageimages)
        result.append(
            caption.data.PageContentCaption(
                page=page.page,
                content=processed,
            ))

    dumped = caption.serialize.dump_captions(result)
    return dumped


def process_page(
        page: texmex.PageTextContentNavigator,
        images,
) -> caption.data.Captions:
    """Detect caption below the images."""
    if not images:
        return []
    result = []
    for bounding in images:
        y1 = bounding[3]
        selected = after(page, y1, 100)  # TODO: HOLY VALUE
        if not selected:
            utila.info(f'could not find caption after: {bounding}')
            continue
        line, raw = selected[0]
        raw = raw.text.strip()
        result.append(caption.data.Caption(line=line, raw=raw))
    return result


def after(navigator, current, plus):
    selected = [(index, item)
                for index, item in enumerate(navigator)
                if current <= item.bounding.y1 <= current + plus]
    # TODO: IMPROVE THIS SIMPLE SELECTOR
    valid = [
        item for item in selected
        if any(chunk in item[1].text for chunk in ('Abbildung', 'Abb.'))
    ]
    return valid
