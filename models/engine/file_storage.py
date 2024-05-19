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

    Class Attributes:
        __fp (str): The file to save objects to.
        __o (dict): A dictionary of instantiated objects.
        cd (dict): A dictionary of all the classes.
    """

    __fp = 'file.json'
    __o = {}
    cd = {"BaseModel": BaseModel, "User": User, "Place": Place,
          "Amenity": Amenity, "City": City, "Review": Review,
          "State": State}

    def all(self):
        '''Return dictionary of <class>.<id> : object instance'''
        return self.__o

    def new(self, obj):
        '''Set new __o to existing dictionary of instances'''
        if obj:
            k = f"{obj.__class__.__name__}.{obj.id}"
            self.__o[k] = obj

    def save(self):
        """Save/serialize obj dictionaries to json file"""
        od = {}

        for k, o in self.__o.items():
            od[k] = o.to_dict()
        with open(self.__fp, 'w', encoding="UTF-8") as f:
            json.dump(od, f)

    def reload(self):
        """Deserialize obj dicts back to instances, if it exists"""
        try:
            with open(self.__fp, 'r', encoding="UTF-8") as f:
                nod = json.load(f)
            for k, v in nod.items():
                o = self.cd[v['__class__']](**v)
                self.__o[k] = o
        except FileNotFoundError:
            pass
