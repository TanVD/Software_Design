"""
    Модуль исполняющий команды интерпретатора
"""

from abc import ABCMeta, abstractmethod
from src.interpreter import ICommandInterpreter
from src.pparser import IParser
from src.storage import IStorage


class IExecutor(metaclass=ABCMeta):
    """ Интерфейс исполнителя выражений """

    def __init__(self, command_interpreter: ICommandInterpreter,
                 parser: IParser, storage: IStorage):
        self._command_interpreter = command_interpreter
        self._parser = parser
        self._storage = storage

    @abstractmethod
    def execute_expression(self, expr: str) -> str:
        """ Исполнить выражение и вернуть результат """
        pass


class Executor(IExecutor):
    """ Реализация исполнителя выражений """

    def execute_expression(self, expr: str) -> str:
        tokens = self._parser.tokenize(expr)
        commands = self._command_interpreter.retrieve_commands(iter(tokens))

        result = ""
        for command in commands:
            result = command.execute(result, self._storage)

        return result
