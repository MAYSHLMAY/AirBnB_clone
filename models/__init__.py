#!/usr/bin/python3
"""__init__ magic method starter for models directory"""
from models.engine.file_storage import FileStorage


cont = FileStorage()
cont.reload()
