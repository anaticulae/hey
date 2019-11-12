# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import utila

import hey.textnavigator.style as ts
import words.text


def find_sentences(page: words.text.PageTextWithHeadlines) -> words.text.TextSections: # yapf:disable
    result = []
    for section in page.content:
        lines = []
        current = []
        for seq in section.content:
            if not isinstance(seq, iamraw.Paragraph):
                if current:
                    lines.extend(split_sentences(' '.join(current)))
                    current = []
                lines.append('%du' % seq.container)
                continue
            # skip here to ensure that Undefined Container is added which
            # does not have any content, see commit.
            if seq.content is None:
                continue
            text = ts.remove_highnotes(seq.content)
            text = text.replace(utila.NEWLINE, ' ').strip()
            current.append(text)
        if current:
            lines.extend(split_sentences(' '.join(current)))
            current = []
        result.append(
            words.text.TextSection(
                headline=section.headline,
                content=lines,
            ))
    return result


def visit_sections(page: words.text.PageTextWithHeadlines):
    for section in page.content:
        for seq in section.content:
            if not isinstance(seq, iamraw.Paragraph):
                continue
            # skip here to ensure that Undefined Container is added which
            # does not have any content, see commit.
            # TODO: DO WE NEED THIS HERE?
            if seq.content is None:
                continue
            yield section.headline, seq.content


def split_sentences(text: str) -> typing.List[str]:
    """Split a regular `text` into sentence chunks.

    Args:
        text(str): text to split without any newlines
    Returns:
        list of splitted sentences"""
    # TODO: REPLACE WITH EXTERNAL SMART ALTERNATIVE, facebook, google or
    # something else.
    result = []
    current = []
    tokens = text.split(' ')
    for token in tokens:
        if not token:
            continue
        current.append(token)
        lastchar = token[-1]
        if lastchar == '.':
            if len(token) == 2:
                # W. G.
                continue
            if token in WHITELIST:
                continue
            if token[:-1].isnumeric():
                # 1.; 13.
                continue
        if lastchar in SIGN:
            result.append(' '.join(current))
            current = []
    if current:
        result.append(' '.join(current))
    return result


SIGN = {
    '!',
    '.',
    ':',
    '?',
}

WHITELIST = {
    'Aufl.',
    'Bd.',
    'Co.',
    'Diss.',
    'Dok.',
    'Forts.',
    'Hrsg.',
    'Hrsg.',
    'Jg.',
    'Sp.',
    'Verf.',
    'Verl.',
    'Vol.',
    'a.a.O.',
    'al.',
    'bzw.',
    'etc.',
    'ff.'
    'ggf.',
    'lat.',
    'mind.',
    'o.J.',
    'o.V.',
    'o.V.',
    'o.Ä',
    'usw.',
    'vgl.',
    'z.B.',
}

# a.a.O. = am angeführten Ort
# Jg. = Jahrgang
# Aufl. = Auflage
# o.J. = ohne Jahresangabe
# Bd. = Band
# o.V. = ohne Verfasserangabe
# Diss. = Dissertation
# S. = Seite
# Dok. = Dokument
# s. = siehe
# f. = (die) folgende
# Sp. = Spalte
# Verf. = Verfasser
# Forts. = Fortsetzung
# Verl. = Verlag
# H. = Heft
# Vol. = Volume (Band)
# Hrsg. = Herausgeber
