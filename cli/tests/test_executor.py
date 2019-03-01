from unittest import TestCase

from storage import Storage
from commands import CommandCat, CommandEcho, CommandWC, CommandPwd, \
    CommandExit, CommandDefault
from tokens import TokenInSingleQuotes, TokenInDoubleQuotes, TokenPipe, \
    TokenAssignment, TokenWord
from interpreter import CommandInterpreterWithStorage
from pparser import Parser
from executor import Executor


class TestExecutor(TestCase):
    def test_execute_expression(self):
        storage = Storage(r'\$[^ \'\"$]+')
        commands = [CommandCat, CommandEcho, CommandWC,
                    CommandPwd, CommandExit]
        token_types = [TokenInSingleQuotes, TokenInDoubleQuotes, TokenPipe,
                       TokenAssignment, TokenWord]

        executor = Executor(CommandInterpreterWithStorage
                            (storage, commands, TokenPipe, CommandDefault),
                            Parser(token_types), storage)

        self.assertEqual(executor.execute_expression('echo "Hello, world!"'),
                         'Hello, world!')

        self.assertEqual(executor.execute_expression('FILE=../example.txt'), '')

        self.assertEqual(executor.execute_expression('cat $FILE'),
                         'Some example text')

        self.assertEqual(executor.execute_expression('cat $FILE | wc'),
                         '1 3 17')
