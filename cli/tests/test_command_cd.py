import os
from unittest import TestCase

from src.commands import CommandCd
from src.storage import Storage


class TestCommandCd(TestCase):
    def test_execute(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCd([os.path.dirname(__file__) + '/..'])
        command.execute("", storage)
        self.assertEqual(os.getcwd(), os.path.dirname(os.path.dirname(__file__)))
