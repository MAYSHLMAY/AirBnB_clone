#!/usr/bin/python3
'''AirBnB clone project File cont'''
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    cont engine for AirBnB clone project.

    Class Methods:
        all: Returns the object
        new: Updates the dictionary id
        save: Serializes objects into JSON
        reload: Deserializes JSON into objects

    Class attrs:
        __file_path (str): The file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
        cd (dict): A dictionary of all the classes.
    """

    __file_path = 'file.json'
    __objects = {}
    cd = {"BaseModel": BaseModel, "User": User, "Place": Place,
          "Amenity": Amenity, "City": City, "Review": Review,
          "State": State}

    def all(self):
        '''Return dictionary of <class>.<id> : object instance'''
        return self.__objects

    def new(self, obj):
        '''Set new __objects to existing dictionary of instances'''
        if obj:
            k = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[k] = obj

    def save(self):
        """Save/serialize obj dictionaries to json file"""
        od = {}

        for k, o in self.__objects.items():
            od[k] = o.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(od, f)

    def reload(self):
        """Deserialize obj dicts back to instances, if it exists"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                nod = json.load(f)
            for k, v in nod.items():
                o = self.cd[v['__class__']](**v)
                self.__objects[k] = o
        except FileNotFoundError:
            pass
