# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from iamraw import Font
# TODO: rename in serializeraw package
from serializeraw import load_fonts as load_font_content
from serializeraw import load_fontstore as load_font_header


class FontLookUp:

    def __init__(self, header, pages):
        self.header = header
        self.pages = pages

    def font(self, page_number, container, line, char) -> Font:
        page = self.pages[page_number]
        for item in page:
            cur_container, cur_line, cur_char, cur_font = item
            if container < cur_container:
                continue
            if line < cur_line:
                continue
            if char < cur_char:
                continue
            return self.fromindex(cur_font)
        return None

    def page_iter(self, pagenumber):
        return iter(self.pages[pagenumber])

    def __len__(self) -> int:
        return len(self.pages)

    def fromindex(self, index: int) -> Font:
        return self.header[index]


def create_font_lookup(header: str, content: str) -> FontLookUp:
    fonts = load_font_header(header)
    pages = load_font_content(content)

    result = FontLookUp(fonts, pages)
    return result
