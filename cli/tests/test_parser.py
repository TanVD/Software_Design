from unittest import TestCase

from src.pparser import Parser
from src.tokens import TokenInSingleQuotes, TokenInDoubleQuotes, TokenPipe, \
    TokenAssignment, TokenWord


class TestParser(TestCase):
    def test_tokenize(self):
        parser = Parser([TokenInSingleQuotes, TokenInDoubleQuotes, TokenPipe,
                         TokenAssignment, TokenWord])

        self.assertEqual(len(parser.tokenize("echo 123 | wc")), 4)
        self.assertEqual(len(parser.tokenize("echo \"13 xc kdf akf\" | wc")), 4)
        self.assertEqual(len(parser.tokenize("echo '13 xc kdf akf' | wc")), 4)
        self.assertEqual(len(parser.tokenize("xcv=3234 nnn=123")), 2)
