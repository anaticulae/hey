# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import utila

import sections.feature.section
import tests.resources
import words.headlines.multiline
import words.loader.basic


def test_headlines_multiple_master72_extract_pages_5_7():
    path = tests.resources.MASTER_72PAGES
    pages = tuple(range(5, 7))
    chapters = None

    sections_ = sections.feature.section.sections_frompath(path, pages=pages)
    loaded = words.loader.basic.load_basic_frompath(path, pages=pages)

    strategy = words.headlines.multiline.MultiLine(
        sectionlist=sections_,
        basic=loaded,
        chapters=chapters,
    )
    result = strategy.result(pages=pages)
    result = utila.flatten(result)
    assert len(result) == 3
    headlines = [item.text for item in result]

    expected = [
        '1.2 Aufbau der Arbeit',
        ('2. Das Social Web und die Privatsphäre – '
         'Selbstdarstellungsverhalten der Nutzer aus Sicht von '
         'Massenmedien und Literatur'),
        ('2.1 Web 2.0, Social Web und Social Media: Abgrenzungen und '
         'Definitionen')
    ]

    assert headlines == expected
