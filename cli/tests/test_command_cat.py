from unittest import TestCase

from commands import CommandCat


class TestCommandCat(TestCase):
    def test_execute(self):
        command = CommandCat(['../example.txt'])
        self.assertEqual(command.execute(""), "Some example text")

        command = CommandCat(['dsakfjhakdsljf'])
        self.assertEqual(command.execute(""), "cat: 'dsakfjhakdsljf' "
                                              "No such file or directory")
