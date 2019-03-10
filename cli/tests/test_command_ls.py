import os
from unittest import TestCase

from src.commands import CommandLs
from src.storage import Storage


class TestCommandCd(TestCase):
    def test_execute(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandLs([os.path.dirname(os.path.dirname(__file__))])
        self.assertEqual(command.execute("", storage), "class_diagram.png\nsrc\nREADME.md\ntests")
