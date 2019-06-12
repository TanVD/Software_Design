import os
from unittest import TestCase

from src.commands import CommandCd
from src.storage import Storage


class TestCommandCd(TestCase):
    root = os.path.dirname(os.path.dirname(__file__))

    def test_cd_up_absolute(self):
        os.chdir(self.root)

        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCd([os.path.dirname(__file__) + '/..'])
        command.execute("", storage)
        self.assertEqual(os.getcwd(), os.path.dirname(os.path.dirname(__file__)))

    def test_cd_up(self):
        os.chdir(self.root)

        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCd(['..'])
        command.execute("", storage)
        self.assertEqual(os.getcwd(), os.path.dirname(self.root))

    def test_cd_in_existing(self):
        os.chdir(self.root)

        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCd(['tests'])
        command.execute("", storage)
        self.assertEqual(os.getcwd(), os.path.dirname(__file__))

    def test_cd_in_non_existing(self):
        os.chdir(self.root)

        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCd(['testy'])
        self.assertEqual(command.execute("", storage), "cd: '%s/testy' No such directory\n" % self.root)
