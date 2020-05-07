# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import abc
import dataclasses
import typing

import texmex
import utila

import groupme.toc as gt
import groupme.toc.group
import groupme.toc.lineregex
import groupme.utils


@dataclasses.dataclass
class ExtractionResult:
    content: typing.List[gt.TocLines] = dataclasses.field(default_factory=list)
    invalid: typing.List[typing.Any] = dataclasses.field(default_factory=list)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]  # pylint:disable=E1136


@dataclasses.dataclass
class ExtractionData:
    content: texmex.PageTextContentNavigators = None


ExtractionResults = typing.List[ExtractionResult]


class ExtractorStrategy(abc.ABC):

    def __init__(self, loaded: ExtractionData):
        self.loaded = loaded

    @abc.abstractmethod
    def result(self) -> ExtractionResult:
        pass


def group(extracted: groupme.toc.TocLines) -> ExtractionResult:
    right, invalid = groupme.utils.split(
        extracted,
        key=lambda x: isinstance(x, groupme.toc.TocLine),
    )
    content = groupme.toc.group.group(right)

    result = ExtractionResult(content=content, invalid=invalid)
    return result


def load(content: texmex.PageTextContentNavigators) -> ExtractionData:
    # TODO: RENAME TO CREATE?
    data = ExtractionData(content=content)
    return data


def remove_headline(
        content: texmex.PageTextNavigator) -> texmex.PageTextNavigator:
    """Remove table of content headline to improve extraction result."""
    result = texmex.PageTextNavigator(
        size=(content.width, content.height),
        page=content.page,
    )
    for item in content:
        if item.text == 'Inhaltsverzeichnis':
            continue
        result.insert(item.text, item.style, item.bounding)
    return result


def parse_group(items) -> groupme.toc.TocLines:
    parsed = [groupme.toc.lineregex.parse(item.text) for item in items]
    matched = [item is not None for item in parsed]
    if all(matched):
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
                utila.error('could not group and parse %s' % collected)
            collected = []
            continue
        result.append(parsed_item)
    if collected:
        extracted = group_collection_and_parse(collected)
        if extracted:
            # parsing was successful
            result.append(extracted)
    return result


def group_collection_and_parse(items):
    line = ' '.join([item.text for item in items])
    parsed = groupme.toc.lineregex.parse(line)
    return parsed
