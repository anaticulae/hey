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


@dataclasses.dataclass
class CharStyle:
    start: int
    end: int
    size: float = None
    rise: float = None


@dataclasses.dataclass
class HighNote:
    start: int
    end: int
    value: int


@dataclasses.dataclass
class TextStyle:
    content: typing.List[CharStyle] = dataclasses.field(default_factory=list)

    def __iter__(self):
        for style in self.content:  # pylint:disable=E1133
            yield style

    def __len__(self):
        return len(self.content)

    @classmethod
    def textsizes(cls, item: 'TextStyle', method=max):
        assert isinstance(item, cls), type(item)
        result = [char.size for char in item.content]
        return method(result)

    @classmethod
    def create(cls, start, end, size, rise=0):
        return cls(content=[CharStyle(start, end, size, rise)])


@dataclasses.dataclass
class TextInfo:
    text: str
    bounding: iamraw.BoundingBox = None
    style: TextStyle = None

    @classmethod
    def copy(cls, item):
        return cls(text=item.text, bounding=item.bounding, style=item.style)


def create_textstyle(chars: typing.List[iamraw.Char]) -> TextStyle:
    assert chars
    start, size, rise = 0, chars[0].size, chars[0].rise
    result = []
    for index, char in enumerate(chars[1:], start=1):
        if char.size != size or char.rise != rise:
            style = CharStyle(
                start=start,
                end=index,
                size=size,
                rise=rise,
            )
            result.append(style)
            start, size, rise = index, char.size, char.rise
    if start != len(chars):
        style = CharStyle(
            start=start,
            end=len(chars),
            size=size,
            rise=rise,
        )
        result.append(style)
    return TextStyle(content=result)


HIGHNOTE_MIN_RISE = 5.0  # TODO: HOLY NOTE


def highnotes(info: TextInfo) -> typing.List[int]:
    """Extract `HighNote`s out of text line. A highnote is a number
    which is a reference to an item defined in the footer.

    A HighNote is a number which has a text rise higher than
    `HIGHNOTE_MIN_RISE`.

    Args:
        info(TextInfo): text line which can contain HightNote's
    Returns:
        list of parsed `HighNote`s
    """
    text = info.text
    result = []
    for style in info.style:
        if style.rise <= HIGHNOTE_MIN_RISE:
            continue
        value = text[style.start:style.end]
        try:
            value = int(value)
        except ValueError:
            continue
        note = HighNote(
            start=style.start,
            end=style.end,
            value=value,
        )
        result.append(note)
    return result
