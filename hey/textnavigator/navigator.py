# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import typing

import configo
import iamraw
import serializeraw
import utila

import hey.path
import hey.textnavigator.fonts
import hey.textnavigator.style
import hey.utils

START = 0.0
END = 1.0


class PageTextNavigator:
    """The PageTextNavigator eases to navigate through the textual
    content of a Page. The text is processed from top to down and left
    to right.

    To fill navigator with content use `insert`. Acessing the data is
    possible trough `between`, `before`, `after` or __getitem__.
    """

    def __init__(self, size=None, page=-1):
        """Initialize PageTextNavigator with maximal `size`

        Args:
            size(tuple): maximal width/height of PageTextNavigator
            page(int): page number of PageTextNavigator-instance

        Sizes:
            A4: 210 x 297 mm, 8.26 x 11.69 inch, 595 x 842pt
                                                 612 x 792pt
        """
        if size is None:
            size = (612.0, 792.0)
        self.page = page
        self.data = []
        self.width, self.height = size

    def insert(
            self,
            text: str,
            style: hey.textnavigator.style.TextStyle,
            bounding: iamraw.BoundingBox,
    ):
        """Insert text element top to bottom and left to right.

        Args:
            text(str): content of text chunk
            style: style for every character of `text`
            bounding(iamraw.BoundingBox): position and dimension of text area
        """
        x0, y0, x1, y1 = bounding

        assert 0 <= x0 <= x1, f'0<={x0}<={x1}'
        assert 0 <= y0 <= y1, f'0<={y0}<={y1}'
        # TODO: Substract border to move starting text to (0,0)?. If not,
        # x1 is sometimes higher than self.width.
        assert (x1 - x0) < self.width, f'{x1-x0} < {self.width}'
        assert (y1 - y0) < self.height, f'{y1-y0} < {self.height}'

        position = 0
        for item in self.data:
            pos = item.bounding
            if int(pos.y0) == int(y0):
                if int(x0) <= int(pos.x0):
                    break
            elif y0 <= pos.y0:
                break
            position += 1
        datum = hey.textnavigator.style.TextInfo(
            text=text,
            bounding=bounding,
            style=style,
        )
        self.data.insert(position, datum)

    def between(
            self,
            top: float,
            bottom: float,
            left: float = START,
            right: float = END,
    ) -> list:
        """Return content between to and bottom and left to right in
        range [top(0.0), bottom(1.0)] and [left(0.0), right(1.0)].

        Args:
            top(float): accepted content after top mark
            bottom(float): accepted content before bottom mark
            left(float): accepted content after left mark
            right(float): accepted content before right mark
        Returns:
            list of `TextInfo`
        """
        assert START <= top <= bottom <= END, f'{START}<={top}<={bottom}<={END}'
        assert START <= left <= right <= END, f'{START}<={left}<={right}<={END}'

        before = top * self.height
        after = bottom * self.height
        beforeleft = left * self.width
        afterright = right * self.width

        result = []
        for item in self.data:
            bounding = item.bounding
            # before and after are pixel coordinates
            if not before <= bounding.y0 <= bounding.y1 <= after:
                continue
            if not beforeleft <= bounding.x0 <= bounding.x1 <= afterright:
                continue
            result.append(item.copy())
        return result

    def __getitem__(self, index) -> hey.textnavigator.style.TextInfo:
        return self.data[index]

    def __len__(self) -> int:
        """Count text chunks"""
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    @property
    def dimension(self):
        return iamraw.PageSize(width=self.width, height=self.height)

    def before(self, height: float, width: float = END) -> list:
        """Determine elements on the top of the document

        Args:
            height(float[0.0,1.0]): 0.0 is top, 1.0 is bottom
            width: marker from left to right, return elements [0.0 width]
        Returns:
            list of `TextInfo`
        """
        result = self.between(START, height, left=START, right=width)
        return result

    def after(self, height, width=START):
        """Determine elements after `height` till the bottom of the
        page. Additonal shrink from left to right with `width`."""
        result = self.between(height, END, width, END)
        return result

    def offset(self, top: float, bottom: float) -> typing.Tuple[int, int]:
        """Determine the range of content index which represents the
        dataindex's of [top, bottom]."""
        assert START <= top <= bottom <= END
        after = bottom * self.height
        before = top * self.height  # greater than

        result = []
        for index, item in enumerate(self.data):
            # before and after are pixel coordinates
            if before <= item.bounding.y0 <= item.bounding.y1 <= after:
                result.append(index)
        if not result:
            return None, None
        top, bottom = result[0], result[-1] + 1
        return top, bottom


class PageTextContentNavigator:
    """Iterate over page content without footer and header.

    See: PageTextNavigator"""

    def __init__(
            self,
            textnavigator: PageTextNavigator,
            content: iamraw.Border,
    ):
        """Navigate throw text content, ignore footer and header

        Args:
            textnavigator: `textnavigator` with items are located
                           outside of `content`.
            content: distance from page border which defines start of content.
        """
        msg = 'require `PageTextNavigator` got: %s' % type(textnavigator)
        assert isinstance(textnavigator, PageTextNavigator), msg
        msg = 'require `Border` got: %s' % type(content)
        assert isinstance(content, iamraw.Border), msg
        pagesize = iamraw.PageSize(
            width=textnavigator.width,
            height=textnavigator.height,
        )
        self.content = content
        assert content.bottom >= 100, str(content)  # ensure that are pixel
        top, bottom = topbottom(pagesize, content)
        assert 0 <= top <= bottom <= 1.0, str(top) + str(bottom)
        self._page = textnavigator.page
        self.data = textnavigator.between(top, bottom)
        self._offset = textnavigator.offset(top, bottom)

    @property
    def offset(self):
        return self._offset

    @property
    def page(self):
        return self._page

    @property
    def width(self):
        # TODO: adjust dimension to content border
        return self.content.right

    @property
    def height(self):
        # TODO: adjust dimension to content border
        return self.content.bottom - self.content.top

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)


PageTextNavigators = typing.List[PageTextNavigator]
PageTextContentNavigators = typing.List[PageTextContentNavigator]


def create_pagetextnavigators(
        text: iamraw.Document,
        text_positions,
) -> PageTextNavigators:
    result = []
    for textposition in text_positions:
        navigator = PageTextNavigator(
            size=text.dimension,
            page=textposition.page,
        )
        textid = 0
        content = utila.select_page(text, textposition.page)
        for item in content:
            try:
                lines = item.lines
            except AttributeError:
                continue
            pos = textposition.content[textid]
            for index, line in enumerate(lines):
                bounding = iamraw.split_y(pos, index, len(lines))
                style = hey.textnavigator.style.create_textstyle(line.chars)
                # TODO: Remove strip after container is fixed
                if not line.text.strip():
                    # skip bad removed rawmaker extraction
                    continue
                navigator.insert(
                    text=line.text.strip(),
                    style=style,
                    bounding=bounding,
                )
            textid += 1
        result.append(navigator)

    result = fill_empty_navigators(result, dimension=text.dimension)
    return result


def fill_empty_navigators(
        navigators: PageTextNavigators,
        dimension: iamraw.PageSize,
) -> PageTextNavigators:
    """Some documents contain white pages. White pages contain no
    text and therefore no text_positions. The document [CONTENT,
    WHITEPAGE, CONTENT, CONTENT] produces the pagetextnavigators
    page =[0,2,3]. If we assume that some algorithm requires a
    closed row of navigators this can lead to problems.Therefore we
    insert an empty PageTextNavigator at position 1 to avoid these
    problems.
    """
    if not navigators:
        return []
    # require ascending list for while loop below
    navigators = sorted(navigators, key=lambda x: x.page)
    filled = [navigators[0]]
    for item in navigators[1:]:
        # fill empty
        while filled[-1].page + 1 < item.page:
            navigator = PageTextNavigator(
                size=dimension,
                page=filled[-1].page + 1,
            )
            filled.append(navigator)
        filled.append(item)
    return filled


def create_pagetextnavigators_frompath(
        path: str,
        prefix='',
        pages=None,
) -> PageTextNavigators:
    """Load all resources from one `path` to create PageTextNavigator
    for the selected list of `pages` with an optional `prefix` in loaded
    items.

    Args:
        path(str): Path to folder which contains all data to construct.
        prefix(str): Optional prefix to difference items in folder.
        pages(tuple): Tuple of pages to load.
    Returns:
        A list of selected PageTextNavigators.

    Example:
        rawmaker__oneline_text_text.yaml with `oneline` as prefix to
        separate instances.
    """

    text = hey.path.text(path, prefix=prefix)
    text = serializeraw.load_document(text, pages=pages)

    textposition = hey.path.textposition(path, prefix=prefix)
    textposition = serializeraw.load_textpositions(textposition, pages=pages)

    navigators = create_pagetextnavigators(text, textposition)
    return navigators


def create_pagetextcontentnavigators_frompath(
        path: str,
        prefix='',
        pages=None,
) -> PageTextContentNavigators:
    navigators = create_pagetextnavigators_frompath(
        path=path,
        prefix=prefix,
        pages=pages,
    )
    sizeandborderpath = hey.path.sizeandborder(path, prefix=prefix)
    contentborder = serializeraw.load_pageborders(sizeandborderpath)

    result = []
    for navigator in navigators:
        border = utila.select_page(contentborder, navigator.page)
        result.append(PageTextContentNavigator(navigator, border.border))
    return result


def create_pagetextnavigator_fromstr(content: str, fontsize=12.0):
    result = PageTextNavigator()
    for index, line in enumerate(content.splitlines()):
        bounding = iamraw.BoundingBox(
            x0=50,
            y0=100 + index * 20,
            x1=200,
            y1=100 + (index + 1) * 20,
        )
        content = [hey.textnavigator.style.CharStyle(0, len(line), fontsize, 0)]
        style = hey.textnavigator.style.TextStyle(content=content)
        result.insert(
            text=line,
            bounding=bounding,
            style=style,
        )
    return result


def topbottom(size: iamraw.PageSize, contentborder: iamraw.Border):
    height = size.height
    top, bottom = contentborder.top, contentborder.bottom
    top = percent_from_pagesize(height, top)
    bottom = percent_from_pagesize(height, bottom)
    return top, bottom


def percent_to_pagesize(
        size: float,
        percent: float,
) -> float:
    """Convert a percent value to page coordinates

    The top coordinate starts with 0.0 and ends on the bottom with 1.0.

    Args:
        size(float): paper height/width
        percent(float): [0.0; 1.0] of used size
    Returns:
        percentage page height/width value
    """
    assert size >= 0.0
    assert 0.0 <= percent <= 1.0

    result = (1.0 - percent) * size
    return result


def percent_from_pagesize(size, current) -> float:
    """Determine the percentage value of a pagesize

    Args:
        size(float): size of current page
        current(float): position on page
    Returns:
        value in percent in range of [0.0, 1.0]

    Example:
        size    500
        current 100
        return  0.8%

    Hint:
        The max size start at the top of the page.
    """
    assert size > 0
    assert size >= current
    return current / size


def to_content(navigator: PageTextNavigator,
              ) -> hey.textnavigator.fonts.TextBoundsList:
    result = []
    for item in navigator:
        info = hey.textnavigator.fonts.TextBoundsInfo(
            bounds=item.bounding,
            text=item.text,
        )
        result.append(info)
    return result


# Merge lines with lower distance to one text chunk.
MAX_MERGE_DISTANCE = configo.HV_FLOAT_PLUS(default=3.55).value
MAX_MERGE_HORIZONTALY = configo.HV_FLOAT_PLUS(default=14.0).value


def merge_content(
        text: hey.textnavigator.fonts.TextBoundsList,
        max_x_merge=MAX_MERGE_HORIZONTALY,
        max_y_merge=MAX_MERGE_DISTANCE,
        uindex=None,
) -> hey.textnavigator.fonts.TextBoundsList:
    """Merge content blocks to create greater content blocks depending on
    merge strategy.

    Args:
        text: chunk with iamraw.BoundingBox to merge
        max_x_merge(float): feed distance between the two left sides
        max_y_merge(float): vertical distance between 2 BoundingBoxes to
                            merge them into one
        uindex(list[int]): undefined index to link text(TextBoundsList) with
                           text-source if uindex is None, the `uindex` is an
                           ascending list starting with zero.
    Returns:
        (result, merged) - result is the merged content, merged - stores the
                           uindex which are merged together
    """
    if not text:
        # Nothing to merge
        return []

    # ensure input
    assert all([
        isinstance(item, hey.textnavigator.fonts.TextBoundsInfo)
        for item in text
    ]), str(text)

    uindex = list(range(len(text))) if uindex is None else uindex
    bounds = [item.bounds for item in text]
    font_distance = hey.textnavigator.fonts.fontdistance(bounds)
    feed_distance = hey.textnavigator.fonts.feeddistance(bounds)

    # copy element
    result = [(text[0].bounds, [text[0].text])]
    merged = [[uindex[0]]]
    lines = zip(font_distance, feed_distance)
    for index, (fontdist, feeddist) in enumerate(lines, start=1):
        current_bounds, current_text = text[index].bounds, text[index].text
        if fontdist > max_y_merge:
            # new entree
            result.append((current_bounds, [current_text]))
            merged.append([uindex[index]])
            continue
        if abs(feeddist) > max_x_merge:
            # new entree
            result.append((current_bounds, [current_text]))
            merged.append([uindex[index]])
            continue

        # Merge me
        member_location, member_content = result[-1]
        merger_location, merger_content = text[index].bounds, text[index].text
        member_content.append(merger_content)
        merged[-1].append(uindex[index])
        # merged items together and save them as last item
        result[-1] = (
            iamraw.common_box([member_location, merger_location]),
            member_content,
        )

    result = [
        hey.textnavigator.fonts.TextBoundsInfo(
            text=item[1],
            bounds=item[0],
        ) for item in result
    ]
    return result, merged


def merge_content_join(result):
    result = [
        hey.textnavigator.fonts.TextBoundsInfo(
            text=utila.NEWLINE.join(item.text),
            bounds=item.bounds,
        ) for item in result
    ]
    return result


def navigator_to_bounds(navigator: PageTextNavigator,
                       ) -> typing.List[iamraw.BoundingBox]:
    """Extract list of `BoundingBox` from `PageTextNavigator`"""
    assert isinstance(navigator, (
        PageTextNavigator,
        PageTextContentNavigator,
    )), type(navigator)
    return [item.bounding for item in navigator]


def isnavigator(item):
    return isinstance(item, (
        PageTextNavigator,
        PageTextContentNavigator,
    ))
