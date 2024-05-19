#!/usr/bin/python3
"""user class, subcls of BaseModel
"""

from models.base_model import BaseModel
import json


class User(BaseModel):
    '''subcls of BaseModel class'''

    email = ""
    password = ""
    first_name = ""
    last_name = ""
