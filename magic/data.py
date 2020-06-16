# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import enum
import typing

import utila
import yaml

PageContentContentType = collections.namedtuple(
    'PageContentContentType',
    'page, content',
)

PageContentContentTypes = typing.List[PageContentContentType]


class ContentType(enum.Enum):
    TEXT = enum.auto()
    UNDEFINED = enum.auto()


def load_types(content: str, pages: tuple = None) -> PageContentContentTypes:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.safe_load(content)

    result = []
    for page, pagecontent in loaded:
        if utila.should_skip(page, pages):
            continue
        parsed = types_fromstr(pagecontent)
        result.append(PageContentContentType(page=page, content=parsed))
    return result


def dump_types(items: PageContentContentTypes) -> str:
    result = [(page, types_tostr(content)) for page, content in items]
    dumped = yaml.safe_dump(result, width=200)
    return dumped


def types_fromstr(content: list) -> list:
    """\
    >>> types_fromstr(['TEXT', 'UNDEFINED'])
    [<ContentType.TEXT: 1>, <ContentType.UNDEFINED: 2>]
    """
    result = [ContentType[item] for item in content]
    return result


def types_tostr(items) -> str:
    """\
    >>> types_tostr([ContentType.TEXT, ContentType.UNDEFINED])
    ['TEXT', 'UNDEFINED']
    """
    result = [str(item.name) for item in items]
    return result
