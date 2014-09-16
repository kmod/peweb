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


if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost")
