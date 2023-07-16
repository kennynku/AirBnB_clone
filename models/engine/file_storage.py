#!/usr/bin/python3
"""Implementation of storage"""
import json
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.state import State


class FileStorage:
    """Create a storage engine
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Displays all objects in storage"""
        return FileStorage.__objects

    def new(self, obj):
        """Create new object"""
        cname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(cname, obj.id)] = obj

    def save(self):
        """Serialization"""
        odict = FileStorage.__objects
        # Serialize helper
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as j:
            json.dump(objdict, j)

    def reload(self):
        """Deserialization"""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    # Expands the dictionary format
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
