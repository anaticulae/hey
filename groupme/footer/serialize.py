# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import functools
import typing

import utila
import yaml

import groupme.footer
import groupme.footer.fixed
import groupme.footer.moving
import hey
import hey.cluster
import hey.textnavigator.navigator


def dump_headerfooter(pages) -> str:
    # TODO: Move to iamraw
    result = []
    for page in pages:
        raw_header = _dump_header(page.header)
        raw_footer = _dump_footer(page.footer)

        result.append({
            'page': page.page,
            'header': raw_header,
            'footer': raw_footer,
        })
    return yaml.dump(result)


def _dump_footer(footer):
    if not footer:
        return None
    raw = {
        'begin': footer.begin,
        'end': footer.end,
    }

    if isinstance(footer, groupme.footer.moving.MovingFooterInformation):
        # dump footnotes
        notes = [
            groupme.footer.footnotes.dump_footnote(item)
            for item in footer.notes
        ]
        raw['notes'] = notes

    if isinstance(footer, groupme.footer.pages.PagesFooterInformation):
        raw['page_location'] = footer.page_location

    return raw


def _load_footer(raw):
    if not raw:
        return None
    begin = raw['begin']
    end = raw['end']

    # try to export MovingFooterInformation
    with contextlib.suppress(KeyError):
        notes = raw['notes']
        notes = [groupme.footer.footnotes.load_footnote(item) for item in notes]
        result = groupme.footer.moving.MovingFooterInformation(
            begin=begin,
            end=end,
            notes=notes,
        )
        return result

    # try to export PagesFooterInformation
    with contextlib.suppress(KeyError):
        page_location = raw['page_location']
        result = groupme.footer.pages.PagesFooterInformation(
            begin=begin,
            end=end,
            page_location=page_location,
        )
        return result

    # try to export FixedFooterInformation
    result = groupme.footer.fixed.FixedFooterInformation(
        begin=begin,
        end=end,
    )
    return result


def _dump_header(header):
    if not header:
        return None
    raw = {
        'begin': header.begin,
        'end': header.end,
        'page': _dump_pageinformation(header.page)
    }

    with contextlib.suppress(KeyError):
        raw['undefined'] = [
            _dump_headerinfo_undefined(item) for item in header.undefined
        ]
    with contextlib.suppress(KeyError):
        raw['title'] = _dump_headerinfo_headertitle(header.title)

    return raw


def _load_header(raw):
    if not raw:
        return None
    begin = raw['begin']
    end = raw['end']
    page = _load_pageinformation(raw['page'])

    undefined = None
    with contextlib.suppress(KeyError):
        undefined = [
            _load_headerinfo_undefined(item) for item in raw['undefined']
        ]

    title = None
    with contextlib.suppress(KeyError):
        title = _load_headerinfo_headertitle(raw['title'])

    result = groupme.footer.fixed.FixedHeaderInformation(
        begin=begin,
        end=end,
        page=page,
    )
    if undefined:
        result.undefined = undefined
    if title:
        result.title = title
    return result


def _dump_pageinformation(pageinfo):
    if not pageinfo:
        return None
    raw = {
        'value': pageinfo.value,
        'raw': pageinfo.raw,
    }
    return raw


def _load_pageinformation(raw):
    if not raw:
        return None
    result = groupme.footer.PageInformation(
        value=raw['value'],
        raw=raw['raw'],
    )
    return result


def _dump_headerinfo_undefined(item):
    if item is None:
        return None
    raw = {
        'text': item.text,
    }
    return raw


def _load_headerinfo_undefined(item):
    if item is None:
        return None
    return groupme.footer.headnotes.RawText(text=item['text'])


def _dump_headerinfo_headertitle(item):
    if item is None:
        return None
    raw = {
        'title': item.title,
        'raw': item.raw,
    }
    return raw


def _load_headerinfo_headertitle(item):
    if item is None:
        return None
    result = groupme.footer.headnotes.HeaderTitle(
        title=item['title'],
        raw=item['raw'],
    )
    return result


@functools.lru_cache(maxsize=hey.CACHE_SMALL)
def load_headerfooter(content: str,
                     ) -> typing.List[groupme.footer.PageContentFooterHeader]:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)

    result = []
    for item in loaded:

        pagenumber = item['page']
        assert isinstance(pagenumber, int)

        header = _load_header(item['header'])
        footer = _load_footer(item['footer'])

        result.append(
            groupme.footer.PageContentFooterHeader(
                header=header,
                footer=footer,
                page=pagenumber,
            ))
    return result
