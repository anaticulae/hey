# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pprint import pprint
from typing import List
from typing import Tuple

from iamraw import Border
from serializeraw import load_document
from serializeraw import load_horizontals
from serializeraw import load_pageborders
from utila import info

from groupme.feature.numbers import load_textposition
from hey.document import document_border
from hey.undefined import extract_undefined
from words.feature.headlines import content_border
from words.feature.headlines import load_headlines
from words.feature.text import load_text


def prepare_input(
        extracted_text,
        text,
        text_position,
        border,
        headlines,
        horizontals,
) -> Tuple[List, Border]:
    headlines = load_headlines(headlines)
    extracted_text = load_text(extracted_text, headlines)
    horizontals = load_horizontals(horizontals)
    _, border = load_pageborders(border)
    contentborder = content_border(horizontals, border)
    text = load_document(text)
    text_position = load_textposition(text_position)
    extracted = extract_undefined(
        extracted_text,
        text,
        text_position,
        contentborder=contentborder,
    )
    contentborder = document_border(border)
    return extracted, contentborder


def process_input(extracted, worker, contentborder):
    result = []
    for pagecontent in extracted:
        extracted = worker(pagecontent, contentborder)
        if not extracted and pagecontent:
            # TODO: REMOVE LATER
            page = pagecontent[0][0]
            info('Skip on page: %d' % (page))
            pprint(pagecontent)
            continue
        result.append(extracted)
    return result
