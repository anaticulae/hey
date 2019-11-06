# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import typing

import iamraw
import iamraw.sections

DocumentSections = typing.List[iamraw.DocumentSection]


@dataclasses.dataclass
class MultipleSection:

    start: iamraw.sections.Position
    end: iamraw.sections.Position
    # [0.0 100.0]
    trust: iamraw.sections.Percentage = dataclasses.field(default=0.0, compare=False) # yapf:disable
    content: DocumentSections = dataclasses.field(default_factory=list)

    def __getitem__(self, index):
        return self.content[index]  #  pylint:disable=E1136

    def __len__(self):
        return len(self.content)
