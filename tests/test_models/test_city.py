#!/usr/bin/python3
"""Defines unittests for models/city.py.
Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.cont.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        ciy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(ciy))
        self.assertNotIn("state_id", ciy.__dict__)

    def test_name_is_public_class_attribute(self):
        ciy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(ciy))
        self.assertNotIn("name", ciy.__dict__)

    def test_two_cities_unique_ids(self):
        ciy1 = City()
        ciy2 = City()
        self.assertNotEqual(ciy1.id, ciy2.id)

    def test_two_cities_different_created_at(self):
        ciy1 = City()
        sleep(0.05)
        ciy2 = City()
        self.assertLess(ciy1.created_at, ciy2.created_at)

    def test_two_cities_different_updated_at(self):
        ciy1 = City()
        sleep(0.05)
        ciy2 = City()
        self.assertLess(ciy1.updated_at, ciy2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        ciy = City()
        ciy.id = "123456"
        ciy.created_at = ciy.updated_at = dt
        cystr = ciy.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def test_args_unused(self):
        ciy = City(None)
        self.assertNotIn(None, ciy.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        ciy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(ciy.id, "345")
        self.assertEqual(ciy.created_at, dt)
        self.assertEqual(ciy.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def in_Up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def sep_D(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        ciy = City()
        sleep(0.05)
        first_updated_at = ciy.updated_at
        ciy.save()
        self.assertLess(first_updated_at, ciy.updated_at)

    def test_two_saves(self):
        ciy = City()
        sleep(0.05)
        first_updated_at = ciy.updated_at
        ciy.save()
        second_updated_at = ciy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        ciy.save()
        self.assertLess(second_updated_at, ciy.updated_at)

    def test_save_with_arg(self):
        ciy = City()
        with self.assertRaises(TypeError):
            ciy.save(None)

    def test_save_updates_file(self):
        ciy = City()
        ciy.save()
        cyid = "City." + ciy.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        ciy = City()
        self.assertIn("id", ciy.to_dict())
        self.assertIn("created_at", ciy.to_dict())
        self.assertIn("updated_at", ciy.to_dict())
        self.assertIn("__class__", ciy.to_dict())

    def test_to_dict_contains_added_attrs(self):
        ciy = City()
        ciy.middle_name = "Holberton"
        ciy.my_number = 98
        self.assertEqual("Holberton", ciy.middle_name)
        self.assertIn("my_number", ciy.to_dict())

    def test_to_dict_datetime_attrs_are_strs(self):
        ciy = City()
        cy_dict = ciy.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        ciy = City()
        ciy.id = "123456"
        ciy.created_at = ciy.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(ciy.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        ciy = City()
        self.assertNotEqual(ciy.to_dict(), ciy.__dict__)

    def test_to_dict_with_arg(self):
        ciy = City()
        with self.assertRaises(TypeError):
            ciy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
