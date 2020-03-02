# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import dataclasses
import statistics
import typing

import texmex
import utila

import words.text.parser
import words.text.sentence
import words.text.word


@dataclasses.dataclass
class TextOnPage:
    words_: typing.List[str] = dataclasses.field(default_factory=list)
    sentences_: typing.List[str] = dataclasses.field(default_factory=list)
    paragraphs_: int = None
    headlines_: int = None
    # signs included in sentences
    signs_: words.text.word.Marks = dataclasses.field(default_factory=list)
    # ordinary dots ... which are used in table of content etc.
    dots_: words.text.word.Marks = dataclasses.field(default_factory=list)

    def append_sentence(self, item: str):
        self.sentences_.append(item)  # pylint:disable=E1101

    def append_sign(self, item: str):
        self.signs_.append(item)  # pylint:disable=E1101

    def append_word(self, item: str):
        self.words_.append(item)  # pylint:disable=E1101

    def append_dot(self, item: str):
        self.dots_.append(item)  # pylint:disable=E1101

    @property
    def words(self):
        return [item for item in self.words_]  # pylint:disable=E1133

    @property
    def sentences(self):
        return [item for item in self.sentences_]  # pylint:disable=E1133

    @property
    def signs(self):
        return [item for item in self.signs_]  # pylint:disable=E1133

    @property
    def dots(self):
        return len(self.dots_)

    def __getattr__(self, key: str) -> float:
        action, variable = key.split('_', maxsplit=1)
        try:
            data = self.__dict__[f'{variable}_']
        except KeyError:
            raise AttributeError(f'could not access `{key}``')
        if not data:
            return None
        length = (len(item) for item in data)

        operation = {
            'max': max,
            'min': min,
            'mean': statistics.mean,
            'median': statistics.median,
            'mode': utila.modes,
            'stdev': statistics.stdev,
            'variance': statistics.variance,
        }
        with contextlib.suppress(KeyError):
            result = operation[action](length)
            return utila.roundme(result)
        raise ValueError(f'unsupported operation {action} {variable}')


def textonpage(page: texmex.PageTextNavigator) -> TextOnPage:
    result = TextOnPage()
    for chunk in page:
        text = chunk.text.strip()
        sentences = words.text.sentence.split_sentences(text)
        for item in sentences:
            if not words.text.sentence.is_sentence(item):
                continue
            result.append_sentence(item)

        splitted = words.text.parser.text_to_words(text)
        for item in splitted:
            if isinstance(item, str):
                if len(item) <= 2:
                    # skip parsing errors
                    continue
                result.append_word(item)
                continue
            if item == words.text.word.Mark.FULLSTOP:
                result.append_dot(item)
            if isinstance(item, words.text.word.Mark):
                result.append_sign(item)
                continue
            assert f'supported item {item}'
    return result
