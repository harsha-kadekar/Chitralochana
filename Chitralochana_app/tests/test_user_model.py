######################################################################################################################
# Name: test_user_model.py
# Description: This file will have all the unit test cases for testing user model
# References: Flask web development book
# Date: 11/2/2016
######################################################################################################################

import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    '''
    This class will have all the unit testcases which are necessary to test the User model
    '''
    def test_password_setter(self):
        '''
        This unit test will check if password setter of the User class is working file or not
        :return: if condition if false then throw an assertion error.
        '''
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password(self):
        '''
        This unit test checks if the password is readable.
        If we try to read password then it should raise an Attribute error exception
        :return:
        '''
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        '''
        This unit test case will verify if given the valid password whether
        it rightly says given password is correct or not.
        :return:
        '''
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))


    def test_password_salts_are_random(self):
        '''
        This unit test verifies that even though same password is set by two different users, its
        hashes will be different.
        :return:
        '''
        u1 = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u1.password_hash != u2.password_hash)