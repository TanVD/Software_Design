from unittest import TestCase

from storage import Storage


class TestStorage(TestCase):
    def test_evaluate_variables(self):
        storage = Storage(r'\$[^ \'\"$]+')
        storage['a'] = '123'
        self.assertEqual(storage.evaluate_variables("qwe$a"), "qwe123")
        self.assertEqual(storage.evaluate_variables("$a$a$a"), "123123123")
        self.assertEqual(storage.evaluate_variables("aaa aaa"), "aaa aaa")
