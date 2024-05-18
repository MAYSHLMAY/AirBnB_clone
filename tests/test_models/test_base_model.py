#!/usr/bin/python3
""" testing files """
import unittest
import inspect
import pep8
from models.base_model import BaseModel
from datetime import datetime


class BaseModel_test(unittest.TestCase):
    """ check BaseModel """

    def pytest(self):
        """ testing codestyle """
        pcode = pep8.StyleGuide(quiet=True)
        rest = pcode.check_files(['models/base_model.py',
                                  'models/__init__.py',
                                  'models/engine/file_storage.py'])
        self.assertEqual(rest.total_errors, 0,
                         "Code Style Errors (and warnings) occured")


class test_for_base_model(unittest.TestCase):
    """ Class test for BaseModel """
    my_model = BaseModel()

    def TearDown(self):
        """ delete json file """
        del self.test

    def SetUp(self):
        """ Create instance """
        self.test = BaseModel()

    def test_attr_none(self):
        """None attribute."""
        ob_t = BaseModel(None)
        self.assertTrue(hasattr(ob_t, "id"))
        self.assertTrue(hasattr(ob_t, "created_at"))
        self.assertTrue(hasattr(ob_t, "updated_at"))

    def test_kwargs_constructor_2(self):
        """ check id with data """
        dictonary = {'score': 100}

        ob_t = BaseModel(**dictonary)
        self.assertTrue(hasattr(ob_t, 'id'))
        self.assertTrue(hasattr(ob_t, 'created_at'))
        self.assertTrue(hasattr(ob_t, 'updated_at'))
        self.assertTrue(hasattr(ob_t, 'score'))

    def test_str(self):
        """ Test string """
        dictonary = {'id': 'cc9909cf-a909-9b90-9999-999fd99ca9a9',
                     'created_at': '2025-06-28T14:00:00.000001',
                     '__class__': 'BaseModel',
                     'updated_at': '2030-06-28T14:00:00.000001',
                     'score': 100
                     }

        ob_t = BaseModel(**dictonary)
        out = "[{}] ({}) {}\n".format(type(ob_t).__name__,
                                      ob_t.id,
                                      ob_t.__dict__)

    def test_to_dict(self):
        """ check dict """
        ob_t = BaseModel(score=300)
        n_dict = ob_t.to_dict()

        self.assertEqual(n_dict['id'], ob_t.id)
        self.assertEqual(n_dict['score'], 300)
        self.assertEqual(n_dict['__class__'], 'BaseModel')
        self.assertEqual(n_dict['created_at'], ob_t.created_at.isoformat())
        self.assertEqual(n_dict['updated_at'], ob_t.updated_at.isoformat())

        self.assertEqual(type(n_dict['created_at']), str)
        self.assertEqual(type(n_dict['created_at']), str)

    def test_datetime(self):
        """ check datatime """
        bas1 = BaseModel()
        self.assertFalse(datetime.now() == bas1.created_at)

    def test_BaseModel(self):
        """ check attributes values in a BaseModel """

        self.my_model.name = "Holbie"
        self.my_model.my_number = 100
        self.my_model.save()
        my_model_json = self.my_model.to_dict()

        self.assertEqual(self.my_model.name, my_model_json['name'])
        self.assertEqual(self.my_model.my_number, my_model_json['my_number'])
        self.assertEqual('BaseModel', my_model_json['__class__'])
        self.assertEqual(self.my_model.id, my_model_json['id'])

    def test_savefirst(self):
        """check numbers"""
        with self.assertRaises(AttributeError):
            BaseModel.save([455, 323232, 2323, 2323, 23332])

    def test_savesecond(self):
        """ check string """
        with self.assertRaises(AttributeError):
            BaseModel.save("THIS IS A TEST")

    def test_inst(self):
        """check class """
        ml = BaseModel()
        self.assertTrue(ml, BaseModel)
