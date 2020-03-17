# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import typing

import utila
import yaml


@dataclasses.dataclass(unsafe_hash=True)
class LiteratureReference:

    reference: str = None
    data: str = None

    title: str = None
    year: int = None
    authors: typing.List[str] = dataclasses.field(default_factory=list)


LiteratureReferences = typing.List[LiteratureReference]


def dump_literature_reference(references: LiteratureReferences) -> str:
    dumped = yaml.dump(references)
    return dumped


def load_literature_reference(content: str) -> LiteratureReferences:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)
    return loaded
