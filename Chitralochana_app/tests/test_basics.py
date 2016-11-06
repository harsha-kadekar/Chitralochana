#######################################################################################
# Name: test_basics.py
# Description: This file has unit test cases related to applicaiton creation and exit.
# References: Flask Web Development book
# Date: 11/2/2016
#######################################################################################

import unittest
from flask import current_app
from app import create_app, rel_db

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        rel_db.create_all()

    def tearDown(self):
        rel_db.session.remove()
        rel_db.drop_all()
        self.app_context.pop()

    def test_app_exits(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])