#!/usr/bin/python3
"""Define BaseModel"""

import models
from uuid import uuid4
from datetime import datetime

tform = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel():
    """Base model for all models"""
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel
        """

        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)
            if hasattr(self, "created_at") and \
               type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs
                                                    ["created_at"], tform)
            if hasattr(self, "updated_at") and \
               type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs
                                                    ["updated_at"], tform)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)
            models.storage.save()

    def __str__(self):
        """Prints the instance of the super class"""
        clname = self.__class__.__name__
        return "[{}]({}) {}".format(clname, self.id, self.__dict__)

    def save(self):
        """updates datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Dictionary representation of the instance"""
        rdict = self.__dict__.copy()
        rdict["created_at"] = self.created_at.isoformat()
        rdict["updated_at"] = self.updated_at.isoformat()
        rdict["__class__"] = self.__class__.__name__
        return rdict