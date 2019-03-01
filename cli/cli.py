"""
интерпретатор командной строки, поддерживающий следующие команды:
• cat [FILE] — вывести на экран содержимое файла;
• echo — вывести на экран свой аргумент (или аргументы);
• wc [FILE] — вывести количество строк, слов и байт в файле;
• pwd — распечатать текущую директорию;
• exit — выйти из интерпретатора.
"""

import os
from subprocess import run, PIPE
from storage import Storage
from commands import CommandCat, CommandEcho, CommandWC, CommandPwd, \
    CommandExit, CommandDefault, CommandGrep
from tokens import TokenInSingleQuotes, TokenInDoubleQuotes, TokenPipe, \
    TokenAssignment, TokenWord
from interpreter import CommandInterpreterWithStorage
from pparser import Parser
from executor import Executor


def main_loop():
    """
    Главный цикл интерпретатора
    """

    if os.name == 'nt':  # установка кодировки utf-8 для windows
        run(['chcp', '65001'], stdout=PIPE, shell=True)

    storage = Storage(r'\$[^ \'\"$]+')
    commands = [CommandCat, CommandEcho, CommandWC,
                CommandPwd, CommandExit, CommandGrep]
    token_types = [TokenInSingleQuotes, TokenInDoubleQuotes, TokenPipe,
                   TokenAssignment, TokenWord]

    executor = Executor(CommandInterpreterWithStorage
                        (storage, commands, TokenPipe, CommandDefault),
                        Parser(token_types), storage)

    while True:
        try:
            result = executor.execute_expression(input("> "))
            if result:
                print(result)
        except Exception as error:
            print(str(error))


if __name__ == "__main__":
    main_loop()
