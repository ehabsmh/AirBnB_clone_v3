#!/usr/bin/python3
"""Test cases for app"""

from api.v1 import app
import unittest


class Test_App_Docs(unittest.TestCase):
    def test_module_doc(self):
        app_doc = app.__doc__
        self.assertTrue(app_doc)

    def test_fn_doc(self):
        fn_doc = app.close_storage.__doc__
        self.assertTrue(fn_doc)


if __name__ == "__main__":
    unittest.main()
