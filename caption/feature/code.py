# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila


def work(
    text_oneline: str,
    textposition_oneline: str,
    sizeandborder: str,
    footerheader: str,
    codero: str,
    pages: tuple = None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text_oneline,
        textposition_oneline,
        sizeandborderpath=sizeandborder,
        headerfooterpath=footerheader,
        pages=pages,
    )
    codero = serializeraw.load_codes(codero, pages=pages)
    # determine result
    result = convert_listings(codero, ptcns)
    # dump
    dumped = serializeraw.dump_captions(result)
    return dumped


def convert_listings(codero, ptcns) -> iamraw.PageContentCaptions:
    result = []
    for page in codero:
        ptcn = utila.select_page(ptcns, page.page)
        collected = []
        for poc in page.content:
            no_caption = not poc.caption and poc.caption != 0  # pylint:disable=C2001
            if no_caption:
                continue
            line = poc.caption[0]
            if len(poc.caption) > 1:
                lineend = poc.caption[-1]
            else:
                lineend = line + 1
            raw = ' '.join(item.text.strip() for item in ptcn[line:lineend])
            collected.append(iamraw.Caption(line, lineend, raw=raw))
        if collected:
            result.append(
                iamraw.PageContentCaption(
                    page=page.page,
                    content=collected,
                ))
    return result
