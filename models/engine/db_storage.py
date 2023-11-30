#!/usr/bin/python3
"""Define DBStorage class"""
from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine





class DBStorage:
    """ Initialize DBStorage """
    __engine = None
    __session = None

    def __init__(self):
        """ initialize DBStorage class"""
        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")
        HBNB_ENV = getenv("HBNB_ENV")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                    .format(HBNB_MYSQL_USER,
                                    HBNB_MYSQL_PWD,
                                    HBNB_MYSQL_HOST,
                                    HBNB_MYSQL_DB),
                                    pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        """ query on the current database session (self.__session) all objects depending of the class name """
        if cls is None:
            mydict_query = self.__session.query(User).all()
            mydict_query.extend(self.__session.query(State).all())
            mydict_query.extend(self.__session.query(City).all())
            mydict_query.extend(self.__session.query(Amenity).all())
            mydict_query.extend(self.__session.query(Place).all())
            mydict_query.extend(self.__session.query(Review).all())

        else:
            cls = eval(cls)
            mydict_query = self.__session.query(cls).all()
            return {("{}.{}".format(type(obj).__name__, obj.id)): obj for obj in mydict_query}
        
    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session  """
        self.__session.commit()

    def delete(self, obj=None):
        """  delete from the current database session obj if not None """
        if obj is not None:
            del self.__session

    def reload(self):
        """  create all tables in the database (feature of SQLAlchemy) (WARNING: all classes who inherit from Base must be imported before calling Base.metadata.create_all(engine)
            create the current database session (self.__session) from the engine (self.__engine) by using a sessionmaker """

        Base.metadata.create_all(create_engine)
        Session_maker= sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(Session_maker)
        self.__session = session()

    def close(self):
        """ method to close session """
        self.__session.close()