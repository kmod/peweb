from sqlalchemy import (
        create_engine,
        MetaData,
        Table,
        Column,
        Integer,
        Unicode,
        DateTime,
        Float,
        ForeignKey,
        and_
        )
from sqlalchemy.orm import mapper, relationship, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Shelf(Base):
    __tablename__ = "shelves"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {"id": self.id, "name":self.name}

    @staticmethod
    def deleteShelf(shelf_id):
        session.query(Shelf).filter(Shelf.id==shelf_id).delete()
        session.query(UserShelf).filter(UserShelf.shelf_id==shelf_id).delete()

class UserShelf(Base):
    __tablename__ = "usershelves"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    shelf_id = Column(Integer, ForeignKey("shelves.id"), primary_key=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    def getAllShelves(self):
        return session.query(Shelf).join(UserShelf).filter(UserShelf.user_id==self.id)

    def createShelf(self, data):
        print data
        s = Shelf(**data)
        session.add(s)
        session.flush()
        session.add(UserShelf(user_id=self.id, shelf_id=s.id))

engine = create_engine("sqlite:///data.sqlite3")
engine.echo = True
Base.metadata.create_all(engine)

session = scoped_session(sessionmaker(bind=engine))

if not session.query(Shelf).all():
    session.add(Shelf(u"test shelf 1"))
    session.add(Shelf(u"shelf 2"))

    session.add(UserShelf(user_id=1, shelf_id=1))
    session.add(UserShelf(user_id=1, shelf_id=2))
    session.commit()
