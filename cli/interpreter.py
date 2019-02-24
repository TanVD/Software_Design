"""
    Модуль интерпретатора команд
"""

from abc import ABCMeta, abstractmethod
from typing import List, Type, Iterator, Generator
from tokens import IToken
from commands import ICommand
from storage import IStorage


class ICommandInterpreter(metaclass=ABCMeta):
    """ Интерфейс парсера команд из потока токенов """

    def __init__(self, command_types: List[Type[ICommand]],
                 delimiter: Type[IToken], default: Type[ICommand]):
        self.__commands = dict()
        # заполняем словарь комманд по их именам
        for command in command_types:
            if command != default:
                self.__commands[command.name()] = command

        self.__delimiter = delimiter
        self.__default = default

    @abstractmethod
    def retrieve_commands(self, tokens: Iterator[IToken]) -> \
            Generator[ICommand, None, None]:
        """ Преобразать список токенов в список команд """
        pass

    def default_command(self) -> Type[ICommand]:
        """ Вернуть команду, которая будет выполнена,
            если остальные команды не подойдут """
        return self.__default

    def delimiter(self) -> Type[IToken]:
        """ Вернуть разделитель для команд внутри выражения """
        return self.__delimiter

    def retrieve_command(self, expr: str) -> Type[ICommand]:
        """ Получить класс команды по имени команды """
        return self.__commands.get(expr, self.__default)


class CommandInterpreterWithStorage(ICommandInterpreter):
    """ Реализация парсера команд из потока токенов """

    def __init__(self, storage: IStorage, commands: List,
                 delimiter: Type[IToken], default: Type[ICommand]):
        super().__init__(commands, delimiter, default)
        self.__storage = storage

    def retrieve_commands(self, tokens: Iterator[IToken]) -> \
            Generator[ICommand, None, None]:
        token = next(tokens, None)

        if not token:
            raise StopIteration()

        if not token.is_possibly_command():
            raise RuntimeError("Unexpected token: " + token.get_value())
        else:
            token.eval_vars(self.__storage)
            if token.execute(self.__storage):
                args = []
                if self.retrieve_command(token.get_value()) \
                        == self.default_command():
                    args.append(token.get_value())

                for arg_token in tokens:
                    if arg_token.__class__ != self.delimiter():
                        arg_token.eval_vars(self.__storage)
                        args.append(arg_token.get_value())
                    else:
                        yield self.retrieve_command(token.get_value())(args)
                        yield from self.retrieve_commands(tokens)
                        break
                else:
                    yield self.retrieve_command(token.get_value())(args)
            else:
                yield from self.retrieve_commands(tokens)
