# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import groupme.toc.group
import groupme.toc.lineregex
import groupme.utils


def parse_group(items, page) -> groupme.toc.TocLines:
    assert page is not None, page
    parsed = [groupme.toc.lineregex.parse(item.text) for item in items]
    matched = [item is not None for item in parsed]

    if all(matched):
        for item in parsed:
            item.raw_location = page
        return parsed
    result = []
    collected = []
    for match, item, parsed_item in zip(matched, items, parsed):
        if not match:
            collected.append(item)
            continue
        if match and collected:
            collected.append(item)
            extracted = group_collection_and_parse(collected)
            if extracted:
                result.append(extracted)
            else:
                # log not parsed
                # TODO: USE VERBOSE LEVEL
                utila.error('could not group and parse %s' % collected)
            collected = []
            continue
        result.append(parsed_item)
    if collected:
        extracted = group_collection_and_parse(collected)
        if extracted:
            # parsing was successful
            result.append(extracted)

    # setup parse page location
    for item in result:
        item.raw_location = page
    return result


def group_collection_and_parse(items):
    line = ' '.join([item.text for item in items])
    parsed = groupme.toc.lineregex.parse(line)
    return parsed
