from unittest import TestCase

from commands import CommandEcho


class TestCommandEcho(TestCase):
    def test_execute(self):
        command = CommandEcho(['123', 'asd'])
        self.assertEqual(command.execute(""), "123 asd")
