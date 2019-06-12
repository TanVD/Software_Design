import os
from unittest import TestCase

from src.commands import CommandLs
from src.storage import Storage


class TestCommandLs(TestCase):
    def test_execute(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandLs([os.path.dirname(os.path.dirname(__file__))])

        self.assertEqual(set(command.execute("", storage).split("\n")),
                         {"class_diagram.png", "src", "README.md", "tests"})
