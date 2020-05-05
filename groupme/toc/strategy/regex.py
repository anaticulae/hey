# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""toc - regex extractor
=====================

Extract headlines based on regex pattern.

design decision
---------------

Should we support following whitespaces?

    It is not required to support lines with ending whitespaces. Following
    whitespace puts water into the wine and leads to more missmatchings. The
    better approach is to improve the pdf-parser to avoid following
    whitespaces.

    See: :class:`tests.groupme_.toc.test_regex.test_extract_toc_line_whitespace_decission`.
"""
import copy
import math
import re

import iamraw
import utila

import groupme.toc
import groupme.toc.lineregex as gtl
import groupme.toc.strategy as gts


class RegexTocExtractor(gts.ExtractorStrategy):

    def result(self) -> gts.ExtractionResult:
        pages = []
        for page in self.loaded.content:
            pages.append(utila.NEWLINE.join([item.text for item in page]))

        parsed = [parse(item) for item in pages]
        flat = utila.flatten(parsed)
        grouped = gts.group(flat)
        return grouped


def parse(content: str) -> groupme.toc.TocLines:
    """Parse table of content via regex.

    Args
        content(str): content of block of text
    Returns:
        ordered list form top to down of parse table of content
    Pattern:

        with level:

        .. code-block :: none

            X.      Chapter ........... 1
            X.X     Section . . . . . . 3

        or no level:

        .. code-block :: none

            Eidesstattliche Erklärung ........... 69
    """
    duplicated = content
    result = []
    for pattern in [
            gtl.EXTENDED_PATTERN,
            gtl.EXTENDED_PATTERN_LETTER,
            gtl.DICTONARY,
            gtl.NO_DOTS,
    ]:
        for line in re.finditer(pattern, content):
            item = gtl.extract_match(line)
            result.append(item)
            # remove already matched content to do not confuse lower
            # strict pattern
            content = content.replace(item.raw, '')

    # TODO: improve this
    for line in [item for item in content.splitlines() if item.strip()]:
        if re.match(r'^\d', line):
            continue
        matched = re.match(gtl.NO_LEVEL, line)
        if not matched:
            continue
        matched = gtl.extract_match(matched)
        result.append(matched)

    # remove duplications, which can occur when table of content is on the
    # same page as first headline.
    result = groupme.toc.remove_duplication(result)

    # Ensure that toc list is ordered by position on pdf page
    result = groupme.toc.sort_byposition(result, duplicated)
    return result


def parse_page(page: iamraw.Page) -> groupme.toc.TocLines:
    """Merge `page` to raw string and extract the lines of table of content.

    Hint:
        see `parse`
    """
    # prepare data
    oneline_text = oneline(page)

    result = parse(oneline_text)
    return result


def oneline(page) -> str:
    if isinstance(page, iamraw.Page):
        lines = utila.flatten([
            container for container in page
            if isinstance(container, iamraw.TextContainer)
        ])
        # lines = oneline_merge(lines)
        # TODO: CHECK FOR ONELINE_MERGE
        lines = [item.text for item in lines]
    else:
        # PageTextNavigator
        lines = oneline_merge([item for item in page])
        lines = [item.text for item in lines]
    lines = split_newlines(lines)
    lines = [item.strip() for item in lines]

    text = utila.NEWLINE.join(lines)
    return text


def oneline_merge(lines):
    """Merge layout if required."""
    # TODO: EXPERIMENTAL: IMPROVE, MOVE TO RAWMAKER?
    if not lines:
        return []
    # TODO: REPLACE BY .copy
    lines = [copy.deepcopy(item) for item in lines]
    # left to right
    lines = sorted(lines, key=lambda item: item.bounding.x0)
    # top to down
    lines = sorted(lines, key=lambda item: item.bounding.y0)

    result = [lines[0]]
    for item in lines[1:]:
        last_y = result[-1].bounding.y0
        current_y = item.bounding.y0
        if math.fabs(last_y - current_y) > 5.0:  # TODO: HOLY VALUE
            result.append(item)
            continue
        # TODO: MERGE BOUNDING
        # merge
        result[-1].text = result[-1].text.strip() + ' ' + item.text.strip()

    return result


def split_newlines(items):
    result = []
    for item in items:
        result.extend(item.splitlines())
    return result


MIN_DOTS_IN_TOC_LINE = 4  # TODO: HOLY VALUE


def is_tocline(index, lines) -> bool:

    def tocline(item):
        if item.count('.') < MIN_DOTS_IN_TOC_LINE:
            return False
        # avoid count sentence endings.
        return any((
            item.count('. .') >= (MIN_DOTS_IN_TOC_LINE / 2),
            item.count('..') >= (MIN_DOTS_IN_TOC_LINE / 2),
            item.count('…') >= (MIN_DOTS_IN_TOC_LINE / 2),
        ))

    item = lines[index]
    if tocline(item):
        return True
    try:
        before = lines[index - 1]
        after = lines[index + 1]
    except IndexError:
        return False
    return tocline(before) and tocline(after)
