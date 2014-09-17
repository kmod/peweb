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
        and_,
        Text,
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
        shelf_id = int(shelf_id)
        session.query(Shelf).filter(Shelf.id==shelf_id).delete()
        session.query(UserShelf).filter(UserShelf.shelf_id==shelf_id).delete()

    @staticmethod
    def loadForUser(u, shelf_id):
        shelf_id = int(shelf_id)
        allowed = bool(session.query(UserShelf).filter(UserShelf.shelf_id==shelf_id and UserShelf.user_id==u.id).all())
        assert allowed
        return session.query(Paper).join(ShelfPaper).filter(ShelfPaper.shelf_id==shelf_id)
        # return [dict(id=shelf_id, name="paper %d" % shelf_id, url="http://www.vision.caltech.edu/publications/DollarEtAlECCV08mcl.pdf")]

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

class Paper(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    url = Column(Text, nullable=False)

    def __init__(self, name):
        self.name = name

class ShelfPaper(Base):
    __tablename__ = "shelfpaper"
    shelf_id = Column(Integer, ForeignKey("shelves.id"), primary_key=True)
    paper_id = Column(Integer, ForeignKey("papers.id"), primary_key=True)

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
