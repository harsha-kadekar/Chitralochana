######################################################################################
# Name: test_userModel.py
# Description: This file has unit tests that will test the user database and class
# References: -
# Date: 1/30/2017
######################################################################################

import unittest
from app.models import User


class userModelTestCase(unittest.TestCase):
    '''
    This class has functions which will test the user Model
    '''
    def test_password_setter(self):
        '''
        This will verify if a password is set or not.
        :return: -
        '''
        u = User(password='harsha')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        '''
        This will verify password is write only and cannot be read
        :return: -
        '''
        u = User(password = 'harsha')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        '''
        This will verify set password can be verified properly.
        after setting if correct password is passed then it should
        verify. In case wrong password is sent then it should not
        verify
        :return:
        '''
        u = User(password = 'harsha')
        self.assertTrue(u.verify_password('harsha'))
        self.assertFalse(u.verify_password('kadekar'))

    def test_password_salts_are_random(self):
        '''
        This will test generated password hash are random.
        Even with same password for two different users will have
        two different password hash
        :return:
        '''
        u1 = User(password='harsha')
        u2 = User(password='harsha')
        self.assertTrue(u1.password_hash != u2.password_hash)