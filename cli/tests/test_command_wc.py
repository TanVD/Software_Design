from unittest import TestCase

from commands import CommandWC


class TestCommandWC(TestCase):
    def test_execute(self):
        command = CommandWC(['../example.txt'])
        self.assertEqual(command.execute(""), "1 3 17")

        command = CommandWC([])
        self.assertEqual(command.execute('Some example text'), "1 3 17")

        command = CommandWC(['sdfsdfsdf'])
        self.assertEqual(command.execute(''), "wc: 'sdfsdfsdf'"
                                              " No such file or directory")
