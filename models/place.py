#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv

from sqlalchemy.orm import relationship
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import String, Integer, Float, Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from models.review import Review

metadata = Base.metadata
table_amenity = Table("place_amenity", metadata,
                      Column("place_id", String(60),
                      ForeignKey("places.id"),
                      primary_key=True, nullable=False),
                      Column("amenity_id", String(60),
                      ForeignKey("amenities.id"),
                      primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms =  Column(Integer, default=0, nullable=False)
    max_guest =  Column(Integer, default=0, nullable=False)
    price_by_night =  Column(Integer, default=0, nullable=False)
    latitude =  Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="all, delete")



    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def review(self):
            """ getter attribute reviews that returns
                the list of Review instances with place_id equals 
                to the current Place.id
                => It will be the FileStorage relationship between 
                Place and Review
            """
            list_review = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    list_review.append(review)
            return(list_review)


        @property
        def amenities(self):
            """ Getter attribute amenities that returns 
                the list of Amenity instances based onthe attribute amenity_ids
                that contains all Amenity.id linked to the Place
            """
            list_amenities = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id == self.amenity_ids:
                    list_amenities.append(amenity)
            return(list_amenities)

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)