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

import words.text.sentence


@dataclasses.dataclass
class AbbreviationList:
    data: set = dataclasses.field(default_factory=set)

    def append(self, item):
        self.data.add(item)  # pylint:disable=E1101

    def __contains__(self, item):
        return item in self.data  # pylint:disable=unsupported-membership-test


AbbreviationLists = typing.List[AbbreviationList]

DUDEN = AbbreviationList(data=words.text.sentence.WHITELIST)


@dataclasses.dataclass
class AbbreviationListLookup:
    table: AbbreviationList = dataclasses.field(default=AbbreviationList)
    duden: AbbreviationList = dataclasses.field(default=AbbreviationList)

    def __contains__(self, item):
        return any((
            item in self.duden,  # pylint:disable=unsupported-membership-test
            item in self.table,  # pylint:disable=unsupported-membership-test
        ))

    @classmethod
    def fromparsed(cls, parsed=None):
        if parsed is None:
            parsed = AbbreviationList()
        lookup = cls(table=parsed, duden=DUDEN)
        return lookup
