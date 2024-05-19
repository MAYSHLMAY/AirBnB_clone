#!/usr/bin/python3
"""Defines unittests for models/place.py.
Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.cont.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(ple))
        self.assertNotIn("city_id", ple.__dict__)

    def test_user_id_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(ple))
        self.assertNotIn("user_id", ple.__dict__)

    def test_name_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(ple))
        self.assertNotIn("name", ple.__dict__)

    def test_description_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(ple))
        self.assertNotIn("desctiption", ple.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(ple))
        self.assertNotIn("number_rooms", ple.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(ple))
        self.assertNotIn("number_bathrooms", ple.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(ple))
        self.assertNotIn("max_guest", ple.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(ple))
        self.assertNotIn("price_by_night", ple.__dict__)

    def test_latitude_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(ple))
        self.assertNotIn("latitude", ple.__dict__)

    def test_longitude_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(ple))
        self.assertNotIn("longitude", ple.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        ple = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(ple))
        self.assertNotIn("amenity_ids", ple.__dict__)

    def test_two_places_unique_ids(self):
        ple1 = Place()
        ple2 = Place()
        self.assertNotEqual(ple1.id, ple2.id)

    def test_two_places_different_created_at(self):
        ple1 = Place()
        sleep(0.05)
        ple2 = Place()
        self.assertLess(ple1.created_at, ple2.created_at)

    def test_two_places_different_updated_at(self):
        ple1 = Place()
        sleep(0.05)
        ple2 = Place()
        self.assertLess(ple1.updated_at, ple2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        ple = Place()
        ple.id = "123456"
        ple.created_at = ple.updated_at = dt
        plstr = ple.__str__()
        self.assertIn("[Place] (123456)", plstr)
        self.assertIn("'id': '123456'", plstr)
        self.assertIn("'created_at': " + dt_repr, plstr)
        self.assertIn("'updated_at': " + dt_repr, plstr)

    def test_args_unused(self):
        ple = Place(None)
        self.assertNotIn(None, ple.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        ple = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(ple.id, "345")
        self.assertEqual(ple.created_at, dt)
        self.assertEqual(ple.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

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
        ple = Place()
        sleep(0.05)
        first_updated_at = ple.updated_at
        ple.save()
        self.assertLess(first_updated_at, ple.updated_at)

    def test_two_saves(self):
        ple = Place()
        sleep(0.05)
        first_updated_at = ple.updated_at
        ple.save()
        second_updated_at = ple.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        ple.save()
        self.assertLess(second_updated_at, ple.updated_at)

    def test_save_with_arg(self):
        ple = Place()
        with self.assertRaises(TypeError):
            ple.save(None)

    def test_save_updates_file(self):
        ple = Place()
        ple.save()
        plid = "Place." + ple.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        ple = Place()
        self.assertIn("id", ple.to_dict())
        self.assertIn("created_at", ple.to_dict())
        self.assertIn("updated_at", ple.to_dict())
        self.assertIn("__class__", ple.to_dict())

    def test_to_dict_contains_added_attrs(self):
        ple = Place()
        ple.middle_name = "Holberton"
        ple.my_number = 98
        self.assertEqual("Holberton", ple.middle_name)
        self.assertIn("my_number", ple.to_dict())

    def test_to_dict_datetime_attrs_are_strs(self):
        ple = Place()
        pl_dict = ple.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        ple = Place()
        ple.id = "123456"
        ple.created_at = ple.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(ple.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        ple = Place()
        self.assertNotEqual(ple.to_dict(), ple.__dict__)

    def test_to_dict_with_arg(self):
        ple = Place()
        with self.assertRaises(TypeError):
            ple.to_dict(None)


if __name__ == "__main__":
    unittest.main()
