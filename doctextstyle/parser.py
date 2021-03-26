# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import iamraw
import texmex
import utila

VerticalTextDistance = collections.namedtuple(
    'VerticalTextDistance',
    'top, bottom',
)
VerticalTextDistances = typing.List[VerticalTextDistance]


def parses(
        navigators: texmex.PageTextNavigators,
        magics: iamraw.PageContentContentTypes = None,
        fontstore: iamraw.FontStore = None,
        parser: callable = None,
) -> iamraw.PageTextPropertiesList:
    parser = parser if parser else parse
    magics = magics if magics else []
    result = []
    for navigator in navigators:
        magic = select_magic(magics, navigator.page)
        if fontstore:
            parsed = parser(navigator, magic, fontstore)
        else:
            parsed = parser(navigator, magic)
        result.append(parsed)
    return result


def parse(
        navigator: texmex.PageTextNavigator,
        magic: 'iamraw.PageContentContentType.content',
) -> iamraw.PageTextProperties:
    lengths = textlength(navigator)
    hashed = [item.text.strip() for item in navigator]
    distances = textdistances(navigator)
    sizes = textsizes(navigator)
    fonts = textfonts(navigator)
    vertical = vertical_position(navigator)
    left, right = leftright(navigator)

    equal_length = [
        len(item) for item in [
            lengths,
            hashed,
            sizes,
            fonts,
            distances,
            vertical,
            left,
            right,
        ]
    ]
    assert len(set(equal_length)) == 1, f'different iter length {equal_length}'

    lengths = skip_magic(lengths, magic)
    hashed = skip_magic(hashed, magic)
    sizes = skip_magic(sizes, magic)
    fonts = skip_magic(fonts, magic)
    distances = skip_magic(distances, magic)
    vertical = skip_magic(vertical, magic)
    left = skip_magic(left, magic)
    right = skip_magic(right, magic)

    result = iamraw.PageTextProperties(
        lengths,
        hashed,
        sizes,
        fonts,
        distances,
        vertical,
        left,
        right,
        page=navigator.page,
    )
    return result


def parse_vector(
        navigator: texmex.PageTextNavigator,
        magic: 'iamraw.PageContentContentType.content',
        fontstore: iamraw.FontStore,
) -> iamraw.PageTextProperties:
    rates = textrate(navigator)
    uppers = upperrate(navigator)
    # lengths = textlength(navigator)
    # hashed = [item.text.strip() for item in navigator]
    distances = textdistances(navigator)
    sizes = textsizes(navigator)
    bolds = bold(navigator, fontstore)
    italics = italic(navigator, fontstore)
    fonts = textfonts(navigator, fontstore)
    top, bottom = topbottom(navigator)
    left, right = leftright(navigator)

    equal_length = [
        len(item) for item in [
            sizes,
            fonts,
            distances,
            top,
            bottom,
            left,
            right,
        ]
    ]
    assert len(set(equal_length)) == 1, f'different iter length {equal_length}'

    rates = skip_magic(rates, magic)
    uppers = skip_magic(uppers, magic)
    sizes = skip_magic(sizes, magic)
    bolds = skip_magic(bolds, magic)
    italics = skip_magic(italics, magic)
    fonts = skip_magic(fonts, magic)
    distances = skip_magic(distances, magic)
    top = skip_magic(top, magic)
    bottom = skip_magic(bottom, magic)
    left = skip_magic(left, magic)
    right = skip_magic(right, magic)

    result = [
        sizes,
        bolds,
        italics,
        left,
    ]
    return result


def normalize(items):
    maxed = max(items)
    if maxed:
        items = [item / maxed for item in items]
    return items


def select_magic(magics, page) -> collections.defaultdict:
    selected = utila.select_content(magics, page, default=[])
    result = set()
    for index, magicitem in selected:
        if magicitem not in SKIPPER:
            continue
        result.add(index)
    return result


SKIPPER = {
    iamraw.PageContentType.FIGURE,
    iamraw.PageContentType.FORMULA,
    iamraw.PageContentType.TABLE,
}


def skip_magic(items, magics):
    result = []
    for index, item in enumerate(items):
        if index in magics:
            continue
        result.append(item)
    return result


def document_textdistance(navigators) -> float:
    """Determine the most common text distance"""
    result = []
    for navigator in navigators:
        if not navigator:
            # empty page
            continue
        page_textdistances = textdistances(navigator)
        result.extend(page_textdistances)
    mode = utila.modes(result)
    return mode


def textdistances(navigator, digits: int = 1) -> VerticalTextDistances:
    # TODO: MOVE TO TEXMEX
    if not navigator:
        return []
    if len(navigator) == 1:
        # no predecessor and successor
        return [VerticalTextDistance(None, None)]
    ypos = vertical_position(navigator)

    # first
    result = [VerticalTextDistance(None, ypos[0].bottom - ypos[1].bottom)]
    for before, current, after in zip(ypos[0:-2], ypos[1:-1], ypos[2:]):
        # middles
        top_distance = before.bottom - current.bottom
        bottom_distance = current.bottom - after.bottom
        result.append(VerticalTextDistance(top_distance, bottom_distance))
    # last
    result.append(VerticalTextDistance(ypos[-2].bottom - ypos[-1].bottom, None))

    # round to have propper user output/developer handling
    rounded = round_vertical_distances(result, digits=digits)
    return rounded


def round_vertical_distances(items, digits: int = 1):
    """Round list of `VerticalTextDistances`.

    >>> round_vertical_distances([VerticalTextDistance(1.333, None), VerticalTextDistance(5.88, 5.0)])
    [VerticalTextDistance(top=1.3, bottom=None), VerticalTextDistance(top=5.9, bottom=5.0)]
    """
    result = []
    for item in items:
        before = utila.roundme(
            item[0],
            digits=digits,
        ) if item[0] is not None else None
        after = utila.roundme(
            item[1],
            digits=digits,
        ) if item[1] is not None else None
        result.append(VerticalTextDistance(before, after))

    return result


def textlength(navigator) -> utila.Ints:
    return textvalue(navigator, selector=lambda item: len(item.text.strip()))


def textwidth(navigator) -> utila.Floats:
    return textvalue(
        navigator,
        selector=lambda item: item.bounding.x1 - item.bounding.x0,
    )


def bold(navigator, fontstore) -> utila.Floats:

    def isbold(item):
        font = fontstore[item.style.fontid]
        weight = font.weight
        return 100.0 if weight == iamraw.Weight.BOLD else 0.0

    return textvalue(navigator, selector=isbold)


def italic(navigator, fontstore) -> utila.Floats:

    def isitalic(item):
        font = fontstore[item.style.fontid]
        style = font.style
        return 100.0 if style == iamraw.Style.ITALIC else 0.0

    return textvalue(navigator, selector=isitalic)


def textuppper(navigator) -> utila.Floats:
    result = textvalue(
        navigator,
        selector=lambda item: len([it for it in item.text if it.isupper()]),
    )
    return result


def textrate(navigator) -> utila.Floats:
    widths = textwidth(navigator)
    lengths = textlength(navigator)
    result = [
        width / length if length else 0
        for width, length in zip(widths, lengths)
    ]
    result = utila.roundme(result)
    return result


def upperrate(navigator) -> utila.Floats:
    uppers = textuppper(navigator)
    lengths = textlength(navigator)
    result = [
        upper / length if length else 0
        for upper, length in zip(uppers, lengths)
    ]
    result = utila.roundme(result)
    return result


def textvalue(navigator, selector: callable) -> utila.Ints:
    return [selector(item) for item in navigator]


def textsizes(navi: texmex.NavigatorMixin) -> utila.Floats:
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        # determine most common text size
        fontsizes = [
            [char.size] * (char.end - char.start) for char in line.style
        ]
        fontsizes = utila.flatten(fontsizes)
        collected.append(utila.mode(fontsizes, minimize=True))
    return collected


def textfonts(navi: texmex.NavigatorMixin, fontstore=None) -> utila.Ints:
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        # TODO: REPLACE WITH char.width
        # determine most common font family
        family = [[char.font] * (char.end - char.start) for char in line.style]
        family = utila.flatten(family)
        collected.append(utila.mode(family))
    if fontstore:
        collected = [hash(fontstore[item].name) for item in collected]
    return collected


def topbottom(navigator) -> VerticalTextDistances:
    if not navigator:
        return []
    border = iamraw.Border(0, navigator.width, 0, navigator.height)
    bounds = texmex.textbounds(navigator, border)
    # ignore empty content
    bounds = [item.bounds for item in bounds if len(item.text)]
    tops = [bounds[0].topdist] + utila.diffs([item.topdist for item in bounds])
    tops = utila.roundme(tops)
    bottoms = utila.diffs([item.bottomdist for item in bounds])
    bottoms = bottoms + [bounds[-1].bottomdist]
    bottoms = utila.roundme(bottoms)
    return tops, bottoms


def vertical_position(navigator) -> VerticalTextDistances:
    if not navigator:
        return []
    border = iamraw.Border(0, navigator.width, 0, navigator.height)
    bounds = texmex.textbounds(navigator, border)
    # ignore empty content
    bounds = [item.bounds for item in bounds if len(item.text)]
    dist = [
        VerticalTextDistance(
            item.topdist,
            item.bottomdist,
        ) for item in bounds
    ]
    return dist


def leftright(navigator) -> VerticalTextDistances:
    if not navigator:
        return [], []
    # ignore empty content
    border = iamraw.Border(0, navigator.width, 0, navigator.height)
    bounds = texmex.textbounds(navigator, border)
    bounds = [item.bounds for item in bounds if len(item.text)]
    left = [item.leftdist for item in bounds]
    right = [item.rightdist for item in bounds]
    return left, right
