#!/usr/bin/python3
"""
Unit tests for console using Mock module from python standard library
Checks console for capturing stdout into a StringIO object
"""

import os
import sys
import unittest
# from unittest.mock import create_autospec, patch
from io import StringIO
from console import HBNBCommand
# from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestConsole(unittest.TestCase):
    """
    Unittest for the console model
    """
    pass


if __name__ == '__main__':
    unittest.main()
