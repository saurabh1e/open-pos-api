import unittest
from .test_users import TestSetup\
    , TestSetupFailure, TestRole, TestUser, TestUserRole


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestSetup))
    test_suite.addTest(unittest.makeSuite(TestSetupFailure))
    test_suite.addTest(unittest.makeSuite(TestUser))
    test_suite.addTest(unittest.makeSuite(TestRole))
    test_suite.addTest(unittest.makeSuite(TestUserRole))
    return test_suite
