import os
from unittest import TestCase

from src.commands import CommandCd
from src.storage import Storage


class TestCommandCd(TestCase):
    def test_cd_up_absolute(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCd([os.path.dirname(__file__) + '/..'])
        command.execute("", storage)
        self.assertEqual(os.getcwd(), os.path.dirname(os.path.dirname(__file__)))

    def test_cd_up(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCd(['..'])
        command.execute("", storage)
        self.assertEqual(os.getcwd(), os.path.dirname(os.path.dirname(__file__)))

    def test_cd_in_existing(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCd(['../tests'])
        command.execute("", storage)
        self.assertEqual(os.getcwd(), os.path.dirname(__file__))

    def test_cd_in_non_existing(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCd(['../testy'])
        self.assertEqual(command.execute("", storage), "cd: '%s/../testy' No such directory\n" % os.path.dirname(__file__))
