# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pprint import pformat
from typing import List
from typing import Tuple

from iamraw import Border
from serializeraw import load_document
from serializeraw import load_headlines
from serializeraw import load_horizontals
from serializeraw import load_pageborders
from serializeraw import load_text
from utila import info

import words.headlines
from groupme.feature.numbers import load_textposition
from hey.document import document_border
from hey.undefined import extract_undefined


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
    border = load_pageborders(border)
    contentborder = words.headlines.contentborder(border, horizontals)
    text = load_document(text)
    text_position = load_textposition(text_position)
    extracted = extract_undefined(
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
            info('skip on page: %d' % (page))
            info(pformat(pagecontent))
            continue
        result.append(extracted)
    return result
