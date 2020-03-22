# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Single Page Analysis
====================

Determine the likelihood of beeing a feature based on local page
information.
"""

import dataclasses

import iamraw
import serializeraw
import texmex
import utila

import sections.feature


@dataclasses.dataclass
class Config:
    likelihood_name: str = None
    page_analysis: callable = None

    def __post_init__(self):
        assert callable(self.page_analysis), type(self.page_analysis)  # pylint:disable=E1101


@dataclasses.dataclass
class Data:
    document: str
    position: str
    pages: tuple = None


def work(data: Data, config: Config) -> str:
    assert config.page_analysis

    page_analysis = config.page_analysis

    pages = tuple(data.pages) if data.pages else None
    text = serializeraw.load_document(data.document, pages=pages)
    textposition = serializeraw.load_textpositions(data.position, pages=pages)
    navigators = texmex.create_pagetextnavigators(
        text=text,
        text_positions=textposition,
        fill_empty=False,
    )
    result = {page.page: page_analysis(page) for page in navigators}

    uniformed = sections.feature.multiform_result(result)
    if uniformed is None:
        uniformed = sections.feature.uniform_result(result)

    likelihood = [
        iamraw.PageContentLikelihood(
            page=page,
            content=iamraw.Likelihood(value, config.likelihood_name),
        ) for page, value in uniformed.items()
    ]

    # write result
    dumped = serializeraw.dump_likelihood(likelihood)
    return dumped
