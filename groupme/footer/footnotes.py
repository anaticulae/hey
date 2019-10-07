# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This module parses `FootNotes` out of raw data.

There are 2 supported types of footnotes:

    raw-text:    "Aus Gründen der besseren Lesbarkeit wird hier und im "
    literature: "s. Berg 2013: 2"
                "Gero von Randow, zeit.de, 19.1.2007"


TODO: FOR FURTHER ANALYSIS WE REQUIRE DIFFERENT FOOTER LINE ANALYZER
TODO: SUPPORT MULTILINE FOOTNOTES
"""
import dataclasses
import re

import detector.parser


@dataclasses.dataclass
class FootNote():
    number: int
    text: str
    raw: str
    author: str = None
    title: str = None
    year: int = None


PATTERN = r'^(?P<number>\d{1,3}) (?P<text>[\w\d:\.,;/\(\) ]+)$'
PATTERN = re.compile(PATTERN, re.MULTILINE)


def parse(content: str):
    result = []
    parsed = re.finditer(PATTERN, content)
    for item in parsed:
        number = item['number']
        text = item['text']
        raw = detector.parser.extract_match(item)

        footnote = FootNote(
            number=number,
            text=text,
            raw=raw,
        )
        result.append(footnote)
    return result
