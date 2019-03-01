from unittest import TestCase

from commands import CommandCat
from storage import Storage


class TestCommandCat(TestCase):
    def test_execute(self):
        storage = Storage(r'\$[^ \'\"$]+')

        command = CommandCat(['../example.txt'])
        self.assertEqual(command.execute("", storage), "Some example text")

        command = CommandCat(['dsakfjhakdsljf'])
        self.assertEqual(command.execute("", storage), "cat: 'dsakfjhakdsljf' "
                                                       "No such file or directory")
