"""
    Модуль парсера токенов
"""

from abc import ABCMeta, abstractmethod
import itertools
import copy
import re
from typing import List, Type, Iterator
from tokens import IToken


class IParser(metaclass=ABCMeta):
    """ Интерфейс парсера для токенов """

    def __init__(self, token_types: List[Type[IToken]]):
        # сортируем по приоритету
        self._token_types = sorted(token_types,
                                   key=lambda token_cls: token_cls.priority())

    @abstractmethod
    def tokenize(self, expression: str) -> List[IToken]:
        """ Парсинг токенов из выражения """
        pass


class Parser(IParser):
    """ Реализация парсера токенов """

    def tokenize(self, expression: str) -> List[IToken]:
        def tokenize_with_types(expr: str, token_types: Iterator[Type[IToken]]) \
                -> List[IToken]:
            """ Рекурсивно парсим выражение по приориету токенов,
                каждый токен разбивает выражение на два подвыражения и т.д. """
            tokens = []
            token_class = next(token_types, None) \
 \
                    if expr and token_class:
                        tokens_of_type = re.findall(token_class.regexp(), expr)

                        # удаляем группы из регулярного выражения, чтобы не было
                        # лишней информации в подвыражениях
                        split_by = re.sub(r'(?<!\\)(\(|\))', '',
                                          token_class.regexp())
                        tokens_not_of_type = re.split(split_by, expr)

                        for not_token, token in itertools.zip_longest(
                                tokens_not_of_type,
                                tokens_of_type,
                                fillvalue=[]):
                            tokens += tokenize_with_types(not_token,
                                                          copy.copy(
                                                              token_types))
                            if token:
                                tokens.append(token_class(token))

            return tokens

        return tokenize_with_types(expression, iter(self._token_types))
