#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.
Unittest classes:
    TFS
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TFS(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def tfs_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def tfs_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def tfsoips(self):
        self.assertEqual(str, type(FileStorage._FileStorage__fp))

    def tfsoipdict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def ts_init(self):
        self.assertEqual(type(models.cont), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def in_Up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def sep_D(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def fiall(self):
        self.assertEqual(dict, type(models.cont.all()))

    def fiall_with_arg(self):
        with self.assertRaises(TypeError):
            models.cont.all(None)

    def test_new(self):
        ba_m = BaseModel()
        us = User()
        st = State()
        pl = Place()
        ciy = City()
        amn = Amenity()
        rv = Review()
        models.cont.new(ba_m)
        models.cont.new(us)
        models.cont.new(st)
        models.cont.new(pl)
        models.cont.new(ciy)
        models.cont.new(amn)
        models.cont.new(rv)
        self.assertIn("BaseModel." + ba_m.id, models.cont.all().keys())
        self.assertIn(ba_m, models.cont.all().values())
        self.assertIn("User." + us.id, models.cont.all().keys())
        self.assertIn(us, models.cont.all().values())
        self.assertIn("State." + st.id, models.cont.all().keys())
        self.assertIn(st, models.cont.all().values())
        self.assertIn("Place." + pl.id, models.cont.all().keys())
        self.assertIn(pl, models.cont.all().values())
        self.assertIn("City." + ciy.id, models.cont.all().keys())
        self.assertIn(ciy, models.cont.all().values())
        self.assertIn("Amenity." + amn.id, models.cont.all().keys())
        self.assertIn(amn, models.cont.all().values())
        self.assertIn("Review." + rv.id, models.cont.all().keys())
        self.assertIn(rv, models.cont.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.cont.new(BaseModel(), 1)

    def test_save(self):
        ba_m = BaseModel()
        us = User()
        st = State()
        pl = Place()
        ciy = City()
        amn = Amenity()
        rv = Review()
        models.cont.new(ba_m)
        models.cont.new(us)
        models.cont.new(st)
        models.cont.new(pl)
        models.cont.new(ciy)
        models.cont.new(amn)
        models.cont.new(rv)
        models.cont.save()
        down = ""
        with open("file.json", "r") as f:
            down = f.read()
            self.assertIn("BaseModel." + ba_m.id, down)
            self.assertIn("User." + us.id, down)
            self.assertIn("State." + st.id, down)
            self.assertIn("Place." + pl.id, down)
            self.assertIn("City." + ciy.id, down)
            self.assertIn("Amenity." + amn.id, down)
            self.assertIn("Review." + rv.id, down)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.cont.save(None)

    def test_reload(self):
        """
        Tests method: reload (reloads objects from string file)
        """
        a_storage = FileStorage()
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        with open("file.json", "w") as f:
            f.write("{}")
        with open("file.json", "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(a_storage.reload(), None)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.cont.reload(None)


if __name__ == "__main__":
    unittest.main()
