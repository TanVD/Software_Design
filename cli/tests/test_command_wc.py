from unittest import TestCase

from src.commands import CommandWC
from src.storage import Storage


class TestCommandWC(TestCase):
    def test_execute(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandWC(['example.txt'])
        self.assertEqual(command.execute("", storage), "1 3 17")

        command = CommandWC([])
        self.assertEqual(command.execute('Some example text', storage),
                         "1 3 17")

        command = CommandWC(['sdfsdfsdf'])
        self.assertEqual(command.execute('', storage), "wc: 'sdfsdfsdf'"
                                                       " No such file or directory")
