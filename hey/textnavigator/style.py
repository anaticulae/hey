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
import utila
import yaml


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


HighNotes = typing.List[HighNote]


@dataclasses.dataclass
class TextStyle:
    content: typing.List[CharStyle] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if not self.content:
            return
        last = self.content[0]  # pylint:disable=E1136
        for current in self.content[1:]:  # pylint:disable=E1136
            assert current.start < current.end, current
            assert current.start == last.end, f'{current.start} == {last.end}'
            last = current

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


def highnotes(info: TextInfo) -> HighNotes:
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


def remove_highnotes(info: TextInfo) -> str:
    """Replace hight notes with empty character. Therefore the text
    width is shrinked.

    Args:
        info(TextInfo): text data with rise information
    Returns:
        text without any hightnotes
    """
    notes = highnotes(info)
    result = []
    current = 0
    for item in notes:
        result.append(info.text[current:item.start])
        current = item.end
    if current != len(info.text):
        result.append(info.text[current:])
    return ''.join(result)


@dataclasses.dataclass
class PageContentTextItems:
    page: int
    content: list = dataclasses.field(default_factory=list)


def load_highnotes(content: str, pages: tuple = None):
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)
    result = []
    for pagecontent in loaded:
        pagenumber = int(pagecontent['page'])
        if utila.should_skip(pagenumber, pages):
            continue
        page = PageContentTextItems(page=pagenumber)
        page.content = [
            HighNote(
                start=item['start'],
                end=item['end'],
                value=item['value'],
            ) for item in pagecontent['content']
        ]
        result.append(page)
    return result


def dump_highnotes(pages) -> str:
    assert all([isinstance(item, PageContentTextItems) for item in pages])
    result = []
    for page in pages:
        raw = {'page': page.page}
        items = [{
            'start': item.start,
            'end': item.end,
            'value': item.value
        } for item in page.content]
        raw['content'] = items
        result.append(raw)
    dumped = yaml.dump(result)
    return dumped
