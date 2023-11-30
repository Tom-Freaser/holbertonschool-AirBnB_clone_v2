#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
import models
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from models.city import City



class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states" 
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """ getter attribute cities that returns the list of City instances with state_id 
                equals to the current State.id =>
                It will be the FileStorage relationship between State and City 
            """
            list_city = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    list_city.append(city)
            return(list_city)
