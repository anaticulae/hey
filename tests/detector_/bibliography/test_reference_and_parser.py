# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import detector.bibliography.reference.freeand as freeand

LONGTEXT = """\
Rumph, H.-J., Hapke, U. & John, U. (1997). Lübecker Alkoholabhängigkeits- und
-missbrauchs-Screening-Test. Göttingen: Hogrefe Verlag GmbH & Co. KG.

Schmidt, R., Dettmeyer, R., Padosch, S. & Madea, B. (2004). Beweiswert
rechtsmedizinischer Begutachtungskriterien zur Feststellung der relativen
alkoholbedingten Fahruntüchtigkeit. Blutalkohol, 41, 1-10.

Schnabel, Eva (2011). Alcohol and driving-related performance - A
comprehensive meta-analysis focussing the significance of the
nonsignificant. Unveröffentlichte Dissertation, Philosophische Fakultät
II der Julius Maximilians-Universität, Würzburg.
""".split('\n\n')


@pytest.mark.parametrize('text, title, authors, pages, year, publisher', [
    pytest.param(
        LONGTEXT[0],
        'Lübecker Alkoholabhängigkeits- und -missbrauchs-Screening-Test',
        [['Rumph', 'H.-J.'], ['Hapke', 'U.'], ['John', 'U.']],
        None,
        1997,
        None,
        id='luebecker',
    ),
    pytest.param(
        LONGTEXT[1],
        ('Beweiswert rechtsmedizinischer Begutachtungskriterien zur '
         'Feststellung der relativen alkoholbedingten Fahruntüchtigkeit'),
        [['Schmidt', 'R.'], ['Dettmeyer', 'R.'], ['Padosch', 'S.'],
         ['Madea', 'B.']],
        None,
        2004,
        None,
        id='schmidt',
    ),
    pytest.param(
        LONGTEXT[2],
        ('Alcohol and driving-related performance - A comprehensive '
         'meta-analysis focussing the significance of the nonsignificant'),
        [['Schnabel', 'Eva']],
        None,
        2011,
        None,
        id='schnabel',
    ),
])
def test_parse_freeand_long(text, title, authors, pages, year, publisher):  # pylint:disable=W0613
    extracted = freeand.parse_longtext(text)
    print(extracted)
    if title:
        assert extracted.title == title
    if pages:
        assert extracted.page == pages[0]
        if len(pages) == 2:
            assert extracted.pageend == pages[1]
    if year:
        assert extracted.year == year
    if authors:
        assert extracted.authors == authors
