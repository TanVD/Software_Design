import os
from unittest import TestCase

from src.commands import CommandCat
from src.storage import Storage


class TestCommandCat(TestCase):
    def test_execute(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCat([os.path.dirname(__file__) + '/example.txt'])
        self.assertEqual(command.execute("", storage), "Some example text")

        command = CommandCat(['dsakfjhakdsljf'])
        self.assertEqual(command.execute("", storage), "cat: 'dsakfjhakdsljf' "
                                                       "No such file or directory")
