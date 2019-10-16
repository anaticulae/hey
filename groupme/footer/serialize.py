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
    }
    return raw


def _load_header(raw):
    if not raw:
        return None
    begin = raw['begin']
    end = raw['end']

    result = groupme.footer.fixed.FixedHeaderInformation(
        begin=begin,
        end=end,
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
