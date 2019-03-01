from unittest import TestCase

from src.storage import Storage
from src.commands import CommandCat, CommandEcho, CommandWC, CommandPwd, \
    CommandExit, CommandDefault
from src.tokens import TokenInSingleQuotes, TokenInDoubleQuotes, TokenPipe, \
    TokenAssignment, TokenWord
from src.interpreter import CommandInterpreterWithStorage
from src.pparser import Parser
from src.executor import Executor


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

        self.assertEqual(executor.execute_expression('FILE=example.txt'), '')

        self.assertEqual(executor.execute_expression('cat $FILE'),
                         'Some example text')

        self.assertEqual(executor.execute_expression('cat $FILE | wc'),
                         '1 3 17')
