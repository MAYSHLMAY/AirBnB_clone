#!/usr/bin/python3
""" testing Place """
import unittest
import pep8
from models.place import Place

class Place_test(unittest.TestCase):
    """ check BaseModel """

    def pytest(self):
        """ testing codestyle """
        pcode = pep8.StyleGuide(quiet=True)
        path_user = 'models/place.py'
        result = pcode.check_files([path_user])
        self.assertEqual(result.total_errors, 0,
                         "Code Style Errors (and warnings) occured")
