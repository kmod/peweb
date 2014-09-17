import functools
import time

try:
    import simplejson as json
except ImportError:
    import json

import flask
app = flask.Flask(__name__)

import model

request = flask.request

def endpoint(*args, **kw):
    login_required = kw.pop("login_required", True)

    def wrapper(f):
        u = model.User(id=1)

        @app.route(*args, **kw)
        @functools.wraps(f)
        def inner(*args, **kw):
            # time.sleep(0.1)
            try:
                r = f(u, *args, **kw)
            except:
                model.session.rollback()
                raise
            model.session.commit()
            return r

        return inner

    return wrapper

@endpoint("/")
def index(u):
    return open("static/main.html").read()

def _user_shelves(u):
    shelves = u.getAllShelves()
    return json.dumps([s.serialize() for s in shelves])

@endpoint("/shelves")
def shelves(u):
    return _user_shelves(u)

@endpoint("/login", login_required=False)
def login():
    return "404"

@endpoint("/create_shelf", methods=["POST"])
def create_shelf(u):
    u.createShelf(request.form.to_dict())

    return _user_shelves(u)

@endpoint("/delete_shelf", methods=["POST"])
def delete_shelf(u):
    d = request.form.to_dict()
    shelf_id = d.pop("shelf_id")
    assert not d

    model.Shelf.deleteShelf(shelf_id)

    return _user_shelves(u)

@endpoint("/shelf")
def shelf_contents(u):
    d = request.args.to_dict()
    shelf_id = d.pop('id')
    assert not d

    assert model.Shelf.authorizedForUser(u, shelf_id)
    return json.dumps([p.serialize() for p in model.Shelf.loadForUser(u, shelf_id)])

@endpoint("/add_paper", methods=["POST"])
def add_paper(u):
    d = request.form.to_dict()
    shelf_id = d.pop("shelf_id")
    paper_data = d.pop("data")
    assert not d

    assert model.Shelf.authorizedForUser(u, shelf_id)
    p = model.Paper.create(paper_data)
    Shelf.addPaper(p)
    return json.dumps([p.serialize() for p in model.Shelf.loadForUser(u, shelf_id)])


if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost")
