from unittest import TestCase

from commands import CommandCat, CommandExit, CommandEcho, CommandWC, \
    CommandPwd, CommandDefault
from interpreter import CommandInterpreterWithStorage
from pparser import Parser
from storage import Storage
from tokens import TokenInSingleQuotes, TokenInDoubleQuotes, TokenPipe, \
    TokenAssignment, TokenWord


class TestCommandInterpreterWithStorage(TestCase):
    def test_retrieve_commands(self):
        storage = Storage(r'\$[^ \'\"$]+')
        commands = [CommandCat, CommandEcho, CommandWC,
                    CommandPwd, CommandExit]
        parser = Parser([TokenInSingleQuotes, TokenInDoubleQuotes, TokenPipe,
                         TokenAssignment, TokenWord])
        interpreter = CommandInterpreterWithStorage(storage, commands,
                                                    TokenPipe, CommandDefault)

        tokens = parser.tokenize("echo 123 | exit | wc | cat | pwd | sdfxvc")
        commands = list(interpreter.retrieve_commands(iter(tokens)))

        self.assertEqual(len(commands), 6)
        self.assertEqual(commands[0].__class__, CommandEcho)
        self.assertEqual(commands[1].__class__, CommandExit)
        self.assertEqual(commands[2].__class__, CommandWC)
        self.assertEqual(commands[3].__class__, CommandCat)
        self.assertEqual(commands[4].__class__, CommandPwd)
        self.assertEqual(commands[5].__class__, CommandDefault)
