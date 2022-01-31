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
import texmex
import utila


def work(
    text_oneline: str,
    textposition_oneline: str,
    sizeandborder: str,
    footerheader: str,
    codero: str,
    translation: str = None,
    pages: tuple = None,
) -> str:
    if not utila.exists(codero):
        utila.error(f'codero does not exists, skip --code: {codero}')
        return serializeraw.dump_captions([])
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text_oneline,
        textposition_oneline,
        sizeandborderpath=sizeandborder,
        headerfooterpath=footerheader,
        pages=pages,
    )
    if utila.exists(translation):
        translation = serializeraw.load_translations(translation, pages=pages)
    else:
        translation = None
    codero = serializeraw.load_codes(codero, pages=pages)
    # determine result
    result = convert_listings(codero, ptcns, translation=translation)
    # dump
    dumped = serializeraw.dump_captions(result)
    return dumped


def convert_listings(
    codero,
    ptcns,
    translation=None,
) -> iamraw.PageContentCaptions:
    translation = texmex.TranslationLookup(translations=translation)
    result = []
    for page in codero:
        ptcn = utila.select_page(ptcns, page.page)
        top = ptcn.offset[0]
        if top is None:
            # TODO: MAY A ROTATED PAGE?
            # NAVIGATOR DOES NOT MATCH TO CODE EXTRACTION
            utila.error(f'empty navigator on page: {page.page}')
            top = 0
        collected = []
        for poc in page.content:
            no_caption = not poc.caption and poc.caption != 0  # pylint:disable=C2001
            if no_caption:
                continue
            # TODO: REMOVE TOP HACK
            line = poc.caption[0]
            line = translation(page.page, line + top) - top
            if len(poc.caption) > 1:
                lineend = poc.caption[-1]
                lineend = translation(page.page, lineend + top) - top
            else:
                lineend = line + 1
            raw = ' '.join(item.text.strip() for item in ptcn[line:lineend])
            collected.append(
                iamraw.Caption(
                    line,
                    lineend,
                    raw=raw,
                    typ=iamraw.CaptionType.CODE,
                ))
        if collected:
            result.append(
                iamraw.PageContentCaption(
                    page=page.page,
                    content=collected,
                ))
    return result
