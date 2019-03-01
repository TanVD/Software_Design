"""
    Модуль для работы с переменными окружения
"""

import re
from abc import ABCMeta, abstractmethod


class IStorage(metaclass=ABCMeta):
    """ Интерфейс для хранения и доступа к переменным окружения """

    @abstractmethod
    def __init__(self, regexp: str):
        """ regexp - регулярное выражение для поиска переменных окружения """
        pass

    @abstractmethod
    def __contains__(self, item: str) -> bool:
        """ Проверка наличия переменной в окружении """
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: str) -> None:
        """ Добавить или обновить переменную окружения """
        pass

    @abstractmethod
    def __getitem__(self, key: str):
        """ Запросить значение переменной окружения """
        pass

    @abstractmethod
    def evaluate_variables(self, expression: str) -> str:
        """ Заменить переменные окружения на их значения из хранилища
            возвращает новую строку с проведенной заменой """
        pass


class Storage(IStorage):
    """ Реализация интерфейса для хранения и доступа к переменным окружения """

    def __init__(self, regexp: str):
        self.__storage = dict()
        self.__regexp = regexp

    def __contains__(self, key: str) -> bool:
        return key in self.__storage

    def __setitem__(self, key: str, value: str) -> None:
        self.__storage[key] = value

    def __getitem__(self, key: str) -> str:
        return self.__storage[key]

    def evaluate_variables(self, expression: str) -> str:
        return re.sub(self.__regexp,
                      lambda var: self.__storage.get(var.group()[1:], ""),
                      expression)
