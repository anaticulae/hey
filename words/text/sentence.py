# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw
import utila

import words.text

SPACE = ' '

# TODO: add more special chars
SPECIAL_CHARS = ['>', '<', r'\)', r'\(']
SPECIAL_CHARS = '|'.join(SPECIAL_CHARS)

NEW_SENTENCE = [
    r'[\w' + SPECIAL_CHARS + r']\. ',
    r'[\w' + SPECIAL_CHARS + r']\.$',
    r'\? ',
    r'\?$',
    r'\w: ',
    r'\w:$',
]
PATTERN = '|'.join(NEW_SENTENCE)


def find_sentences(page: words.text.PageTextWithHeadlines) -> words.text.TextSections: # yapf:disable
    result = []
    for (headline, sequence) in page.content:
        lines = []
        for seq in sequence:
            if not isinstance(seq, iamraw.Paragraph):
                lines.append('%du' % seq.container)
                continue
            # skip here to ensure that Undefined Container is added which
            # does not have any content, see commit.
            if seq.content is None:
                continue
            line = ''.join([item for (item, _) in seq.content])
            line = line.replace(utila.NEWLINE, SPACE)
            last = 0
            for item in re.finditer(PATTERN, line):
                _, end = item.start(), item.end()
                lines.append(line[last:end])
                last = end
            no_match = line == line[last:]
            if no_match:
                utila.error(f'No sentence, maybe a headline: "{line}"?')
            if line[last:]:
                lines.append(line[last:])
        # remove `space` after text
        lines = [item.strip() for item in lines]
        result.append(
            words.text.TextSection(
                headline=headline,
                content=lines,
            ))
    return result
