#!/usr/bin/python3
'''AirBnB clone project File Storage'''
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """ This is a storage engine for AirBnB clone project

    Class Methods:
        all: Return the obj
        new: update the dict id
        save: Serializes, Python objs into JSON strs
        reload: Deserializes, JSON strs into Python objs
    Class Attributes:
        __f_path (str): The name of the file to save objs to.
        _objs (dict): A dict of objs.
        c_dict (dict): A dict of all the classes.
    """

    __f_path = 'file.json'
    _objs = {}
    c_dict = {"BaseModel": BaseModel, "User": User, "Place": Place,
              "Amenity": Amenity, "City": City, "Review": Review,
              "State": State}

    def all(self):
        '''Return dict of <class>.<id> : object instance'''
        return self._objs

    def new(self, obj):
        '''Set new _objs to existing dict of instances'''
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self._objs[key] = obj

    def save(self):
        """Save/serialize obj dictionaries to json file"""
        obj_dict = {}

        for key, obj in self._objs.items():
            obj_dict[key] = obj.to_dict()
        with open(self.__f_path, 'w', encoding="UTF-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserialize/convert obj dicts back to instances, if it exists"""
        try:
            with open(self.__f_path, 'r', encoding="UTF-8") as file:
                new_obj_dict = json.load(file)
            for key, value in new_obj_dict.items():
                obj = self.c_dict[value['__class__']](**value)
                self._objs[key] = obj
        except FileNotFoundError:
            pass
