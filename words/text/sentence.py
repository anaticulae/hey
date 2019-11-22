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
import words.utils.headline as wuh


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


def visit_sentences(
        page: words.text.PageTextWithHeadlines,
        skip_undefined: bool = False,
):
    for section in page.content:
        current = []
        for seq in section.content:
            if not isinstance(seq, iamraw.Paragraph):
                if current:
                    for sentence in split_sentences(' '.join(current)):
                        yield section.headline, sentence
                if not skip_undefined:
                    yield section.headline, f'{seq.container}u'
                continue
            text = ts.remove_highnotes(seq.content)
            text = text.replace(utila.NEWLINE, ' ').strip()
            current.append(text)
        if current:
            for sentence in split_sentences(' '.join(current)):
                yield section.headline, sentence


def merge_sentences(
        pages: words.text.PageTextWithHeadlines,
        skip_undefined: bool = False,
):
    assert len(pages) >= 2, 'require at least two `pages`'
    for current, after in zip(pages[0:-1], pages[1:]):
        current = list(visit_sentences(current, skip_undefined=skip_undefined))
        after = list(visit_sentences(after, skip_undefined=skip_undefined))
        for headline, sentence in current[0:-1]:
            yield headline, sentence
        # TODO: DIRTY
        last = current[-1]
        first = after[0]
        current_headline = last[0]
        if not is_sentence_closed(current[-1]):
            # merge sentence
            assert last
            assert first
            yield current_headline, last[1] + ' ' + first[1]
        else:
            # new page with headline start
            yield last
            if current_headline != first[0]:
                current_headline = first[0]
            yield current_headline, first[1]
        # use headline of the page before to first headline of after page
        for headline, sentence in after[current_headline.end + 1:]:
            if headline != current_headline:
                if headline.text is not None:
                    # do not replace headlines from page before with
                    # virtual none-headlines after page break.
                    current_headline = headline
            yield current_headline, sentence


def visit_chapters(pages):
    current = None
    collected = []
    for headline, sentence in merge_sentences(pages):
        if not wuh.is_higherequal(headline, current):
            # Avoid to add headlines twice. This can happen when merge
            # page 1->2 and 2->3, therefore some lines of page 2 are added
            # twice. This is avoidable when adding headlines strict
            # ascending.
            continue
        if current is None:
            # start
            current = headline
        if headline != current and headline.text is not None:
            yield current, collected
            collected = []
            current = headline
        collected.append(sentence)
    if collected:
        yield current, collected


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
        token = token.lower()  # make approach more robust
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


def is_sentence_closed(token: list) -> bool:
    """Check that the last character of the last token of a sentences contains
    a sentence close sign."""
    assert token, 'empty sentence'
    last = token[-1].strip()
    last_char = last[-1]
    return last_char in SIGN


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
WHITELIST = {item.lower() for item in WHITELIST}

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
