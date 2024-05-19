#!/usr/bin/python3
"""
City class, a subcls of BaseModel
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    A subcls of BaseModel class
    Public class attrs:
        state_id: (str) will be State.id
        name:     (str)
    """
    state_id = ""
    name = ""
