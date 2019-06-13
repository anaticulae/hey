# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from functools import partial

from iamraw import Document
from pytest import fixture
from serializeraw import load_document
from utila import run_command

from sections import PROCESS_NAME
from sections.command import main
from sections.font import FontLookUp
from sections.font import create_font_lookup
from tests.groupme_ import FOOTER_FONT_CONTENT
from tests.groupme_ import FOOTER_FONT_HEADER
from tests.groupme_ import FOOTER_TEXT

#pylint:disable=C0103
run_sections_success = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=True,
)

run_sections_failure = partial(
    run_command,
    main=main,
    process=PROCESS_NAME,
    success=False,
)


@fixture
def restructured_document() -> Document:
    loaded = load_document(FOOTER_TEXT)
    return loaded


@fixture
def restructured_fontlookup() -> FontLookUp:
    lookup = create_font_lookup(FOOTER_FONT_HEADER, FOOTER_FONT_CONTENT)
    return lookup
