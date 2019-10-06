# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pprint
import typing

import iamraw
import serializeraw
import utila

import groupme.feature
import hey.undefined
import words.headlines


def prepare_input(
        extracted_text,
        text,
        text_position,
        border,
        headlines,
        headerfooters,
) -> typing.Tuple[typing.List, iamraw.Border]:
    headlines = serializeraw.load_headlines(headlines)
    extracted_text = serializeraw.load_text(extracted_text, headlines)
    border = serializeraw.load_pageborders(border)
    headerfooters = groupme.footer.load_headerfooter(headerfooters)
    contentborder = words.headlines.contentborder(
        border,
        headerfooters,
    )
    text = serializeraw.load_document(text)
    text_position = serializeraw.load_textpositions(text_position)
    extracted = hey.undefined.extract_undefined(
        extracted_text,
        text,
        text_position,
        contentborder=contentborder,
    )
    return extracted, contentborder


def process_input(extracted, worker):
    result = []
    for pagecontent in extracted:
        extracted = worker(pagecontent)
        if not extracted and pagecontent:
            # TODO: REMOVE LATER
            page = pagecontent[0][0]
            utila.info('skip on page: %d' % (page))
            utila.info(pprint.pformat(pagecontent))
            continue
        result.append(extracted)
    return result
