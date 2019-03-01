from unittest import TestCase

from src.commands import CommandEcho
from src.storage import Storage


class TestCommandEcho(TestCase):
    def test_execute(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandEcho(['123', 'asd'])
        self.assertEqual(command.execute("", storage), "123 asd")
