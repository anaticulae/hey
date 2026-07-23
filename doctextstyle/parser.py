# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import iamraw
import texmex
import utilo

VerticalTextDistance = collections.namedtuple(
    'VerticalTextDistance',
    'top, bottom',
)
VerticalTextDistances = list[VerticalTextDistance]


def parses(
    navigators: texmex.PTNs,
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
    navigator: texmex.PTN,
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
    navigator: texmex.PTN,
    magic: 'iamraw.PageContentContentType.content',
    fontstore: iamraw.FontStore,
) -> iamraw.PageTextProperties:
    if not navigator:
        # empty page
        return []
    rates = textrate(navigator)
    uppers = upperrate(navigator)
    # lengths = textlength(navigator)
    # hashed = [item.text.strip() for item in navigator]
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
            top,
            bottom,
            left,
            right,
        ]
    ]
    assert len(set(equal_length)) == 1, f'different iter length {equal_length}'

    rates: list = skip_magic(rates, magic, zeros=True)
    uppers: list = skip_magic(uppers, magic, zeros=True)
    sizes = skip_magic(sizes, magic, zeros=True)
    bolds = skip_magic(bolds, magic, zeros=True)
    italics = skip_magic(italics, magic, zeros=True)
    fonts = skip_magic(fonts, magic, zeros=True)
    top = skip_magic(top, magic, zeros=True)
    bottom = skip_magic(bottom, magic, zeros=True)
    left = skip_magic(left, magic, zeros=True)
    right = skip_magic(right, magic, zeros=True)

    result = [
        sizes,
        bolds,
        italics,
        left,
        uppers,
    ]
    return result


def normalize(items):
    maxed = max(items)
    if maxed:
        items = [item / maxed for item in items]
    return items


def select_magic(magics, page) -> collections.defaultdict:
    selected = utilo.select_content(magics, page, default=[])
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


def skip_magic(items, magics, zeros: bool = False):
    result = []
    for index, item in enumerate(items):
        if index in magics:
            if zeros:
                # TODO: ??? GOOD IDEA ???
                result.append(0)
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
    mode = utilo.modes(result)
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
        before = utilo.roundme(
            item[0],
            digits=digits,
        ) if item[0] is not None else None
        after = utilo.roundme(
            item[1],
            digits=digits,
        ) if item[1] is not None else None
        result.append(VerticalTextDistance(before, after))

    return result


def textlength(navigator) -> utilo.Ints:
    return textvalue(navigator, selector=lambda item: len(item.text.strip()))


def textwidth(navigator) -> utilo.Floats:
    return textvalue(
        navigator,
        selector=lambda item: item.bounding.x1 - item.bounding.x0,
    )


def bold(navigator, fontstore) -> utilo.Floats:

    bold_ = 100.0
    no_bold = 10.0

    def more_than_eighty_or_nothing(items):
        """Detecting bold requires that more than eigthy percent of the
        characters are bold. In some bolded headlines there are spaces
        characters which are not bold and in some sentences only some
        words are bold."""
        counter = collections.Counter()
        for item in items:
            counter[item] += 1
        item, count = counter.most_common(n=1)[0]
        if count < 0.8 * len(items):
            return set(items)
        return {item}

    def isbold(item):
        fontids = texmex.TextStyle.fontids(
            item.style,
            more_than_eighty_or_nothing,
        )
        if len(fontids) > 1:
            return no_bold
        font = fontstore[item.style.fontid]
        weight = font.weight
        return bold_ if weight == iamraw.Weight.BOLD else no_bold

    return textvalue(navigator, selector=isbold)


def italic(navigator, fontstore) -> utilo.Floats:

    def isitalic(item):
        font = fontstore[item.style.fontid]
        style = font.style
        return 100.0 if style == iamraw.Style.ITALIC else 10.0

    return textvalue(navigator, selector=isitalic)


def textuppper(navigator) -> utilo.Floats:
    result = textvalue(
        navigator,
        selector=lambda item: len([it for it in item.text if it.isupper()]),
    )
    return result


def textrate(navigator) -> utilo.Floats:
    widths = textwidth(navigator)
    lengths = textlength(navigator)
    result = [
        width / length if length else 0
        for width, length in zip(widths, lengths)
    ]
    result = utilo.roundme(result, convert=False)
    return result


def upperrate(navigator) -> utilo.Floats:
    uppers = textuppper(navigator)
    lengths = textlength(navigator)
    result = [
        100 if length >= 5 and (upper / length) > 0.4 else 10
        for upper, length in zip(uppers, lengths)
    ]
    result = utilo.roundme(result, convert=False)
    return result


def textvalue(navigator, selector: callable) -> utilo.Ints:
    return [selector(item) for item in navigator]


def textsizes(navi: texmex.NavigatorMixin) -> utilo.Floats:
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        # determine most common text size
        fontsizes = [
            [char.size] * (char.end - char.start) for char in line.style
        ]
        fontsizes = utilo.flat(fontsizes)
        collected.append(utilo.mode(fontsizes, minimize=True))
    return collected


def textfonts(navi: texmex.NavigatorMixin, fontstore=None) -> utilo.Ints:
    assert issubclass(navi.__class__, texmex.NavigatorMixin), type(navi)
    collected = []
    for line in navi:
        # determine most common font family
        family = [[char.font] * char.width for char in line.style]
        family = utilo.flat(family)
        collected.append(utilo.mode(family))
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
    tops = [bounds[0].topdist]
    if len(bounds) > 1:
        tops.extend(utilo.diffs([item.topdist for item in bounds]))
    tops: list = utilo.roundme(tops, convert=False)
    bottoms = []
    if len(bounds) > 1:
        bottoms.extend(utilo.diffs([item.bottomdist for item in bounds]))
    bottoms.append(bounds[-1].bottomdist)
    bottoms: list = utilo.roundme(bottoms, convert=False)
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
