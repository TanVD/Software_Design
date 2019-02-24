"""
    Модуль с токенамами с которыми работает интерпретатор
"""

from abc import ABCMeta, abstractmethod
from storage import IStorage


class IToken(metaclass=ABCMeta):
    """ Интерфейс для токена, поиск которого будет выполняться при обработке
        входных данных интерпретатора """

    @abstractmethod
    def __init__(self, regexp_result):
        pass

    @staticmethod
    @abstractmethod
    def priority() -> int:
        """ Приоритет поиска токена во входном выражении
            должен вернуть число от 0 до inf """
        pass

    @staticmethod
    @abstractmethod
    def regexp() -> str:
        """ Регулярное выражение для поиска токена
            результат поиска вернется в метод __init__ """
        pass

    @abstractmethod
    def set_value(self, value: str) -> None:
        """ Установка значения токена """
        pass

    @abstractmethod
    def get_value(self) -> str:
        """ Получение значения токена """
        pass

    @abstractmethod
    def eval_vars(self, storage: IStorage) -> None:
        """ Замена переменных окружения на их значения,
            если это необходимо """
        pass

    @abstractmethod
    def is_possibly_command(self) -> bool:
        """ Возможность токена содержать в себе команду """
        pass

    def execute(self, storage: IStorage) -> bool:
        """ Код, который должен быть исполнен,
            если токен станет командой,
            возвращает true если его нужно исполнить как команду """
        return True


class TokenInSingleQuotes(IToken):
    """ Токен для работы с одинарными кавычками в выражении """

    def __init__(self, regexp_result):
        self.__value = regexp_result if regexp_result else ""

    @staticmethod
    def priority() -> int:
        return 16

    @staticmethod
    def regexp() -> str:
        return '[\']([^\']*)[\']'

    def set_value(self, value: str) -> None:
        self.__value = value

    def get_value(self) -> str:
        return self.__value

    def eval_vars(self, storage: IStorage) -> None:
        pass

    def is_possibly_command(self) -> bool:
        return True


class TokenInDoubleQuotes(IToken):
    """ Токен для двойных кавычек в выражении """

    def __init__(self, regexp_result):
        self.__value = regexp_result if regexp_result else ""

    @staticmethod
    def priority() -> int:
        return 32

    @staticmethod
    def regexp() -> str:
        return '[\"]([^\"]*)[\"]'

    def set_value(self, value: str) -> None:
        self.__value = value

    def get_value(self) -> str:
        return self.__value

    def eval_vars(self, storage: IStorage) -> None:
        self.set_value(storage.evaluate_variables(self.get_value()))

    def is_possibly_command(self) -> bool:
        return True


class TokenPipe(IToken):
    """ Токен для пайпа в выражении"""

    def __init__(self, regexp_result):
        pass

    @staticmethod
    def priority() -> int:
        return 48

    @staticmethod
    def regexp() -> str:
        return '\\|'

    def set_value(self, value: str) -> None:
        pass

    def get_value(self) -> str:
        return '|'

    def eval_vars(self, storage: IStorage) -> None:
        pass

    def is_possibly_command(self) -> bool:
        return False


class TokenAssignment(IToken):
    """ Токен для работы с заданием переменных окружения в выражении """

    def __init__(self, regexp_result):
        self.__var = regexp_result[0] if regexp_result else ""
        self.__val = regexp_result[1] if regexp_result else ""

    @staticmethod
    def priority() -> int:
        return 64

    @staticmethod
    def regexp() -> str:
        return '([^ =]+)=([^ ]*)'

    def set_value(self, value: str) -> None:
        buffer = value.split('=')
        if len(buffer) == 2:
            self.__var = buffer[0]
            self.__val = buffer[1]
        else:
            raise RuntimeError("Invalid value for TokenAssignment: " + value)

    def get_value(self) -> str:
        return self.__var + '=' + self.__val

    def eval_vars(self, storage: IStorage) -> None:
        self.__val = storage.evaluate_variables(self.__val)
        self.__var = storage.evaluate_variables(self.__var)

    def is_possibly_command(self) -> bool:
        return True

    def execute(self, storage: IStorage) -> bool:
        """ Сохранить переменную в окружении """
        storage[self.__var] = self.__val
        return False


class TokenWord(IToken):
    """ Токен для парсинга прочих ключевых слов, которые не подошли под
        остальные токены """

    def __init__(self, regexp_result):
        self.__value = regexp_result if regexp_result else ""

    @staticmethod
    def priority() -> int:
        return 128

    @staticmethod
    def regexp() -> str:
        return '[^ \'\"|]+'

    def set_value(self, value: str) -> None:
        self.__value = value

    def get_value(self) -> str:
        return self.__value

    def eval_vars(self, storage: IStorage) -> None:
        self.set_value(storage.evaluate_variables(self.get_value()))

    def is_possibly_command(self) -> bool:
        return True
