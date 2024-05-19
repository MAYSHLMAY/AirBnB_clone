#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import os
import console
import json
import sys
import unittest
from models import cont
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_prompting(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    @classmethod
    def in_UpClass(self):
        """Set up test"""
        self.typing = console.HBNBCommand()

    @classmethod
    def sep_DClass(self):
        """Remove temporary file (file.json) created as a result"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_docstrings_in_console(self):
        """Test docstrings exist in console.py"""
        self.assertTrue(len(console.__doc__) >= 1)

    def test_docstrings_in_test_console(self):
        """Test docstrings exist in test_console.py"""
        self.assertTrue(len(self.__doc__) >= 1)

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", fd.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Unittests for testing help messages of the HBNB command interpreter."""

    def test_help_quit(self):
        h = "Quit command to exit the program"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("help quit"))

    def test_help_create(self):
        h = ("Create instance specified by user")
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("help create"))

    def test_help_EOF(self):
        h = "EOF signal to exit the program"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))

    def test_help_show(self):
        h = ("Print string repr of a class instance, given id")
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("help show"))

    def test_help_destroy(self):
        h = ("Delete a class instance of a given id, save result"
             " to json file")
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))

    def test_help_all(self):
        h = ("Prints all string representation of all instances based or"
             " not on the class name")
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("help all"))

    def test_help_count(self):
        h = ("Display count of instances specified")
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("help count"))

    def test_help_update(self):
        h = ("Updates an instance based on the class name and id by adding"
             " or updating attribute (save the change into the JSON file)")
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("help update"))

    def test_help(self):
        h = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(h, fd.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    """Unittests for testing exiting from the HBNB command interpreter."""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def in_Up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_create_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_create_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_create_invalid_syntax(self):
        correct = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(correct, fd.getvalue().strip())
        correct = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(fd.getvalue().strip()))
            testKey = "BaseModel.{}".format(fd.getvalue().strip())
            self.assertIn(testKey, cont.all().keys())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(fd.getvalue().strip()))
            testKey = "User.{}".format(fd.getvalue().strip())
            self.assertIn(testKey, cont.all().keys())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(fd.getvalue().strip()))
            testKey = "State.{}".format(fd.getvalue().strip())
            self.assertIn(testKey, cont.all().keys())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(fd.getvalue().strip()))
            testKey = "City.{}".format(fd.getvalue().strip())
            self.assertIn(testKey, cont.all().keys())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(fd.getvalue().strip()))
            testKey = "Amenity.{}".format(fd.getvalue().strip())
            self.assertIn(testKey, cont.all().keys())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(fd.getvalue().strip()))
            testKey = "Place.{}".format(fd.getvalue().strip())
            self.assertIn(testKey, cont.all().keys())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(fd.getvalue().strip()))
            testKey = "Review.{}".format(fd.getvalue().strip())
            self.assertIn(testKey, cont.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Unittests for testing show from the HBNB command interpreter"""

    @classmethod
    def in_Up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_show_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(".show()"))

    def test_show_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["BaseModel.{}".format(testID)]
            command = "show BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["BaseModel.{}".format(testID)]
            command = "BaseModel.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["User.{}".format(testID)]
            command = "User.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["State.{}".format(testID)]
            command = "State.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Place.{}".format(testID)]
            command = "Place.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["City.{}".format(testID)]
            command = "City.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Amenity.{}".format(testID)]
            command = "Amenity.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Review.{}".format(testID)]
            command = "Review.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), fd.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Unittests for testing destroy from the HBNB command interpreter."""

    @classmethod
    def in_Up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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
        cont.reload()

    def test_destroy_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_destroy_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_destroy_id_missing_space_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_destroy_id_missing_dot_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_destroy_invalid_id_space_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_destroy_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["BaseModel.{}".format(testID)]
            command = "destroy BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())

    def test_destroy_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["BaseModel.{}".format(testID)]
            command = "BaseModel.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["User.{}".format(testID)]
            command = "User.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["State.{}".format(testID)]
            command = "State.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Place.{}".format(testID)]
            command = "Place.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["City.{}".format(testID)]
            command = "City.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Amenity.{}".format(testID)]
            command = "Amenity.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            obj = cont.all()["Review.{}".format(testID)]
            command = "Review.destory({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, cont.all())


class TestHBNBCommand_all(unittest.TestCase):
    """Unittests for testing all of the HBNB command interpreter."""

    @classmethod
    def in_Up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def fiall_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(correct, fd.getvalue().strip())

    def fiall_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))

    def fiall_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))

    def fiall_single_object_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", fd.getvalue().strip())
            self.assertNotIn("User", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())

    def fiall_single_object_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", fd.getvalue().strip())
            self.assertNotIn("User", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", fd.getvalue().strip())
            self.assertNotIn("BaseModel", fd.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def in_Up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_update_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            """self.assertEqual(correct, fd.getvalue().strip())"""

    def test_update_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            """self.assertEqual(correct, fd.getvalue().strip())"""

    def test_update_missing_id_space_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self):
        correct = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = fd.getvalue().strip()
            testCmd = "update BaseModel {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = fd.getvalue().strip()
            testCmd = "update User {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testId = fd.getvalue().strip()
            testCmd = "update State {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testId = fd.getvalue().strip()
            testCmd = "update City {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = fd.getvalue().strip()
            testCmd = "update Amenity {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = fd.getvalue().strip()
            testCmd = "update Place {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self):
        correct = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create BaseModel")
            testId = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            testCmd = "update BaseModel {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create User")
            testId = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            testCmd = "update User {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create State")
            testId = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            testCmd = "update State {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create City")
            testId = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            testCmd = "update City {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create Amenity")
            testId = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            testCmd = "update Amenity {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create Place")
            testId = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            testCmd = "update Place {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create Review")
            testId = fd.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fd:
            testCmd = "update Review {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, fd.getvalue().strip())

    def test_update_valid_string_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create BaseModel")
            testId = fd.getvalue().strip()
        testCmd = "update BaseModel {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = cont.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create User")
            testId = fd.getvalue().strip()
        testCmd = "update User {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = cont.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create State")
            testId = fd.getvalue().strip()
        testCmd = "update State {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = cont.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create City")
            testId = fd.getvalue().strip()
        testCmd = "update City {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = cont.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create Place")
            testId = fd.getvalue().strip()
        testCmd = "update Place {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = cont.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create Amenity")
            testId = fd.getvalue().strip()
        testCmd = "update Amenity {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = cont.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create Review")
            testId = fd.getvalue().strip()
        testCmd = "update Review {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = cont.all()["Review.{}".format(testId)].__dict__
        self.assertTrue("attr_value", test_dict["attr_name"])

    def test_update_valid_float_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            HBNBCommand().onecmd("create Place")
            testId = fd.getvalue().strip()
        testCmd = "update Place {} latitude 7.2".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = cont.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

    @classmethod
    def in_Up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

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

    def test_count_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))

    def test_count_object(self):
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as fd:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))


if __name__ == "__main__":
    unittest.main()
