#!/usr/bin/python3
"""
The console v: 0.0.1
Contains the entry point of the command interpreter
"""

import cmd


# from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """
    Custom console class
    """

    prompt = '(hbnb) '


if __name__ == '__main__':
    HBNBCommand().cmdloop()
