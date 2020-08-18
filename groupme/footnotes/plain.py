# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw

NUMBER_TEXT = r'(?P<number>\d+)[ ]*(?P<text>.{3,})'


def parse(content: list) -> list:
    collected = merges(content)
    result = []
    # parse footnote
    for multiline in collected:
        text = ''.join([item.text for item in multiline])
        matched = re.match(NUMBER_TEXT, text, flags=re.MULTILINE | re.DOTALL)
        if not matched:
            number, content = -1, text
        else:
            number, content = int(matched['number']), matched['text']
        footnote = iamraw.FootRawNote(
            number=number,
            text=content.strip(),
            style=None,
        )
        result.append(footnote)
    return result


def merges(content):
    if not content:
        return []
    collected = [[content[0]]]
    # merge multiple lines
    for line in content[1:]:
        text = line.text.strip()
        matched = re.match(NUMBER_TEXT, text, re.MULTILINE)
        if not matched:
            collected[-1].append(line)
        else:
            collected.append([line])
    return collected
