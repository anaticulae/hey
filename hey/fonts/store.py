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
from serializeraw import load_font_content
from serializeraw import load_font_header
from utila import NEWLINE


class FontStore:

    def __init__(self, header, pages):
        """Define `FontStore`

        Args:
            header:
            pages:
        """
        self.header = header
        self.pages = pages

    def font(
            self,
            number: int,
            container: int,
            line: int,
            char: int,
    ) -> int:
        fontid = self.fontid(number, container, line, char)
        return self[fontid]

    def fontid(
            self,
            number: int,
            container: int,
            line: int,
            char: int,
    ) -> int:
        """Extract `Font` out out text position

        Args:
            number(int): `number` of given page
            container(int):
            line(int):
            char(int):
        Returns:
            Font
        """
        # TODO: linear complexity!
        page = self.pages[number]
        for item in page:
            cur_container, cur_line, cur_char, cur_font = item
            if cur_container > container:
                return cur_font
            if cur_container == container:
                if cur_line > line:
                    return cur_font
                if cur_line == line:
                    if char >= cur_char:
                        continue
                    return cur_font
                continue
            else:
                continue

        return None

    def fromstr(
            self,
            page: int,
            container: int,
            line: int,
            text: str,
    ) -> Font:
        result = []
        current = self.font(page, container, line, 0)
        collector = ''
        lines = text.splitlines()
        for linenumber, textline in enumerate(lines, start=line):
            for index, item in enumerate(textline, start=0):
                font = self.font(page, container, linenumber, index)
                if font != current:
                    result.append((
                        collector,
                        current,
                    ))
                    collector = item
                    current = font
                else:
                    collector += item
            if linenumber + 1 < len(lines):
                # last item neeeds no newline
                collector += NEWLINE
        # Final font
        if collector:
            result.append((
                collector,
                current,
            ))

        for item in result:
            print(item)
        return result

    def page_iter(self, number):
        return iter(self.pages[number])

    def __len__(self) -> int:
        return len(self.pages)

    def __getitem__(self, index: int) -> Font:
        return self.header[index]


class FontContenStore:

    def __init__(
            self,
            store: FontStore,
            page: int,
            top: float,
            bottom: float,
    ):
        pass


def create_fontstore(header: str, content: str) -> FontStore:
    fonts = load_font_header(header)
    pages = load_font_content(content)

    result = FontStore(fonts, pages)
    return result
