#!/usr/bin/python3
""" testing State """
import unittest
import pep8
from models.state import State

class State_test(unittest.TestCase):
    """ check BaseModel """

    def pytest(self):
        """ testing codestyle """
        pcode = pep8.StyleGuide(quiet=True)
        path_user = 'models/state.py'
        result = pcode.check_files([path_user])
        self.assertEqual(result.total_errors, 0,
                         "Code Style Errors (and warnings) occured")
