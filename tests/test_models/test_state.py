#!/usr/bin/python3
"""Defines unittests for models/state.py.
Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.cont.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        sta = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(sta))
        self.assertNotIn("name", sta.__dict__)

    def test_two_states_unique_ids(self):
        sta1 = State()
        sta2 = State()
        self.assertNotEqual(sta1.id, sta2.id)

    def test_two_states_different_created_at(self):
        sta1 = State()
        sleep(0.05)
        sta2 = State()
        self.assertLess(sta1.created_at, sta2.created_at)

    def test_two_states_different_updated_at(self):
        sta1 = State()
        sleep(0.05)
        sta2 = State()
        self.assertLess(sta1.updated_at, sta2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        sta = State()
        sta.id = "123456"
        sta.created_at = sta.updated_at = dt
        ststr = sta.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dt_repr, ststr)
        self.assertIn("'updated_at': " + dt_repr, ststr)

    def test_args_unused(self):
        sta = State(None)
        self.assertNotIn(None, sta.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        sta = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(sta.id, "345")
        self.assertEqual(sta.created_at, dt)
        self.assertEqual(sta.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        sta = State()
        sleep(0.05)
        first_updated_at = sta.updated_at
        sta.save()
        self.assertLess(first_updated_at, sta.updated_at)

    def test_two_saves(self):
        sta = State()
        sleep(0.05)
        first_updated_at = sta.updated_at
        sta.save()
        second_updated_at = sta.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        sta.save()
        self.assertLess(second_updated_at, sta.updated_at)

    def test_save_with_arg(self):
        sta = State()
        with self.assertRaises(TypeError):
            sta.save(None)

    def test_save_updates_file(self):
        sta = State()
        sta.save()
        stid = "State." + sta.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        sta = State()
        self.assertIn("id", sta.to_dict())
        self.assertIn("created_at", sta.to_dict())
        self.assertIn("updated_at", sta.to_dict())
        self.assertIn("__class__", sta.to_dict())

    def test_to_dict_contains_added_attrs(self):
        sta = State()
        sta.middle_name = "Holberton"
        sta.my_number = 98
        self.assertEqual("Holberton", sta.middle_name)
        self.assertIn("my_number", sta.to_dict())

    def test_to_dict_datetime_attrs_are_strs(self):
        sta = State()
        st_dict = sta.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        sta = State()
        sta.id = "123456"
        sta.created_at = sta.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(sta.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        sta = State()
        self.assertNotEqual(sta.to_dict(), sta.__dict__)

    def test_to_dict_with_arg(self):
        sta = State()
        with self.assertRaises(TypeError):
            sta.to_dict(None)


if __name__ == "__main__":
    unittest.main()
