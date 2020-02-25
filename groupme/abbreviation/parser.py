# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import utila

import groupme.abbreviation
import hey.textnavigator.navigator


def parse(content: hey.textnavigator.navigator.PageTextNavigator):
    result = []
    for line in content:
        raw = line.text
        utila.debug(f'parse: {raw}')
        try:
            short, description = raw.split(maxsplit=1)
        except ValueError:
            if not is_excluded(raw):
                utila.error(f'could not parse: {raw}')
            continue
        if is_excluded(short) or is_excluded(description):
            utila.info(f'skip: {short}, {description}')
            continue
        short, description = short.strip(), description.strip()
        parsed = groupme.abbreviation.Abbreviation(
            short=short,
            description=description,
        )
        utila.debug(f'parsed: {parsed}')
        result.append(parsed)
    return result


def is_excluded(item):
    item = item.strip()
    excluded = {
        'Abkürzung',
        'Abkürzungsverzeichnis',
        'Beschreibung',
        'Glossar',
        'Tabellenverzeichnis',
    }
    return item in excluded
