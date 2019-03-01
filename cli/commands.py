"""
    Модуль с командами с которыми работает интерпретатор
"""
import os
import re
from abc import ABCMeta, abstractmethod
from typing import List
from subprocess import run, PIPE
from storage import IStorage
import argparse


class ICommand(metaclass=ABCMeta):
    """ Интерфейс для команды """

    def __init__(self, args: List[str]):
        self._args = args

    @staticmethod
    @abstractmethod
    def name() -> str:
        """ Вернуть имя команды
            по нему будет происходить разбор команд"""
        pass

    @abstractmethod
    def execute(self, pipe: str, storage: IStorage) -> str:
        """ Выполнить команду с переданным pipeом
            вернуть результат выполнения """
        pass

    def prepend_arg(self, arg: str):
        """ Добавить аргумент перед всеми аргументами """
        self._args = [arg] + self._args

    def append_arg(self, arg: str):
        """ Добавить аргумент после всех аргументов """
        self._args.append(arg)


class CommandCat(ICommand):
    """ Вывести на экран содержимое файла """

    @staticmethod
    def name() -> str:
        return "cat"

    def execute(self, pipe: str, storage: IStorage) -> str:
        if not self._args:
            raise RuntimeError("cat: must specify file names!")

        result = ""
        for filename in self._args:
            try:
                with open(filename) as f:
                    result += f.read() + '\n'
            except IOError as error:
                result += "cat: '%s' No such file or directory\n" % filename

        return result[:-1]


class CommandEcho(ICommand):
    """ Вывести на экран свой аргумент (или аргументы) """

    @staticmethod
    def name() -> str:
        return "echo"

    def execute(self, pipe: str, storage: IStorage) -> str:
        return ' '.join(map(str, self._args))


class CommandWC(ICommand):
    """ Вывести количество строк, слов и байт в файле """

    @staticmethod
    def name() -> str:
        return "wc"

    def execute(self, pipe: str, storage: IStorage) -> str:
        result = ""
        if pipe:
            result += "%d %d %d\n" % (pipe.count('\n') + 1,
                                      len(pipe.split()),
                                      len(pipe))
        else:
            if not self._args:
                raise RuntimeError("wc: must specify file names!")

            for filename in self._args:
                try:
                    with open(filename) as f:
                        data = f.read()
                        result += "%d %d %d\n" % (data.count('\n') + 1,
                                                  len(data.split()),
                                                  len(data))
                except IOError as error:
                    result += "wc: '%s' No such file or directory\n" % filename

        return result[:-1]


class CommandPwd(ICommand):
    """ Распечатать текущую директорию """

    @staticmethod
    def name() -> str:
        return "pwd"

    def execute(self, pipe: str, storage: IStorage) -> str:
        return os.getcwd()


class CommandExit(ICommand):
    """ Выйти из интерпретатора """

    @staticmethod
    def name() -> str:
        return "exit"

    def execute(self, pipe: str, storage: IStorage) -> str:
        quit(0)
        return ""


class CommandDefault(ICommand):
    """ Что будет выполнено, если не одна команда не подойдет """

    @staticmethod
    def name() -> str:
        return ""

    def execute(self, pipe: str, storage: IStorage) -> str:
        process = run(self._args, stdout=PIPE, input=pipe,
                      shell=True, encoding="utf8", errors='ignore')
        return process.stdout


class CommandGrep(ICommand):
    """ Команда grep, ищет паттерн в файле или во входном потоке"""

    @staticmethod
    def name() -> str:
        return "grep"

    def execute(self, pipe: str, storage: IStorage) -> str:
        parser = argparse.ArgumentParser(
            description='Search for PATTERN in each FILE')

        parser.add_argument("-i", "--ignore-case", action="store_true",
                            help="ignore case distinctions")
        parser.add_argument("-w", "--word-regexp", action="store_true",
                            help="force PATTERN to match only whole words")
        parser.add_argument("-A", "--after-context", type=int,
                            help="print NUM lines of output context")
        parser.add_argument("PATTERN",
                            help="PATTERN is an extended regular expression")
        parser.add_argument('FILE', nargs='*',
                            help='FILE is path to file for search')

        try:
            args = parser.parse_args(self._args)
            pattern = args.PATTERN
            result = ""

            if args.word_regexp:
                pattern = r"\b" + pattern + r"\b"

            if args.FILE:
                pipe = ""
                for filename in args.FILE:
                    try:
                        with open(filename, encoding="utf8") as f:
                            pipe += f.read() + '\n'
                    except IOError as error:
                        result += "grep: '%s' No such file or directory\n" % filename

            after_lines_count = 0
            for line in pipe.splitlines(True):
                if re.findall(pattern, line,
                              flags=re.IGNORECASE if args.ignore_case else 0):
                    after_lines_count = args.after_context if args.after_context else 0
                    result += line
                elif after_lines_count > 0:
                    result += line
                    after_lines_count -= 1

            return result[:-1]

        except SystemExit:
            pass

        return ""
