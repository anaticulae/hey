# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from functools import lru_cache

from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load

from hey import CACHE_SMALL
from sections.ctor import Appendix
from sections.ctor import Chapter
from sections.ctor import Content
from sections.ctor import DocumentSection
from sections.ctor import Index
from sections.ctor import Introduction
from sections.ctor import Sections
from sections.ctor import Table
from sections.ctor import TableOfContent
from sections.ctor import Text
from sections.ctor import TitlePage
from sections.ctor import WhitePage

CLASSNAME = '__class__'
SEPCIALFIELD = '__'


def dump_sections(sections: Sections) -> str:
    """Convert `Sections` to raw data"""

    def dump_item(item):
        keys = [key for key in dir(item) if not key.startswith(SEPCIALFIELD)]
        result = {key: item.__getattribute__(key) for key in keys}
        result[CLASSNAME] = item.__class__.__name__
        return result

    result = []
    for page in sections:
        content = dump_item(page)
        content['content'] = [dump_item(item) for item in page.content]
        result.append(content)
    dumped = dump(result)
    return dumped


@lru_cache(CACHE_SMALL)
def load_sections(content: str) -> Sections:
    """Load sections from path or str

    Args:
        content(str):
    Return:
        loaded Sections
    """
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    def generate_ctor():
        """Create table with name[constructor]"""
        items = [
            Appendix, Chapter, Content, DocumentSection, Index, Introduction,
            Sections, Table, TableOfContent, Text, TitlePage, WhitePage
        ]
        return {str(item.__name__): item for item in items}

    _ctor = generate_ctor()

    def load_item(item):

        def determine_type(item):
            """Load items, in special a list entry"""
            if isinstance(item, list):
                # recursive call
                return [load_item(single) for single in item]
            return item

        result = {
            key: determine_type(item[key])
            for key in item.keys()
            if not key.startswith(SEPCIALFIELD)
        }

        ctor = _ctor[item[CLASSNAME]]
        result = ctor(**result)
        return result

    result = Sections()
    for section in loaded:
        result.append(load_item(section))
    return result
