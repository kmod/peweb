from sqlalchemy import (
        create_engine,
        MetaData,
        Table,
        Column,
        Integer,
        String,
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
    name = Column(String(255), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def serialize(self):
        return {"id": self.id, "name":self.name}

class UserShelves(Base):
    __tablename__ = "usershelves"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    shelf_id = Column(Integer, ForeignKey("shelves.id"), primary_key=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    def getAllShelves(self):
        return session.query(Shelf).join(UserShelves).filter(UserShelves.user_id==self.id)

engine = create_engine("sqlite:///data.sqlite3")
engine.echo = True
Base.metadata.create_all(engine)

session = scoped_session(sessionmaker(bind=engine))

if not session.query(Shelf).all():
    session.add(Shelf(1, "test shelf 1"))
    session.add(Shelf(2, "shelf 2"))

    session.add(UserShelves(user_id=1, shelf_id=1))
    session.add(UserShelves(user_id=1, shelf_id=2))
    session.commit()
