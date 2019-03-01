import os
from unittest import TestCase

from src.commands import CommandGrep
from src.storage import Storage


class TestCommandGrep(TestCase):
    def test_execute(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandGrep(['-i', '-w', '-A 2', 'plugin',
                               os.path.dirname(__file__) + '/grep_test'])
        self.assertEqual(command.execute("", storage), "apply plugin: 'java'\n"
                                                       "apply plugin: 'idea'\n"
                                                       "group = 'ru.example'\n"
                                                       "version = '1.0'")

        command = CommandGrep(['-i', '-w', '-A 2', 'plugi',
                               os.path.dirname(__file__) + '/grep_test'])
        self.assertEqual(command.execute("", storage), "")

        command = CommandGrep(['-i', '-w', '-A 2', 'PluGin',
                               os.path.dirname(__file__) + '/grep_test'])
        self.assertEqual(command.execute("", storage), "apply plugin: 'java'\n"
                                                       "apply plugin: 'idea'\n"
                                                       "group = 'ru.example'\n"
                                                       "version = '1.0'")

        command = CommandGrep(
            ['plugin', os.path.dirname(__file__) + '/grep_test'])
        self.assertEqual(command.execute("", storage), "apply plugin: 'java'\n"
                                                       "apply plugin: 'idea'")
