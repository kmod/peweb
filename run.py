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

def login_required(f):
    u = model.User(id=1)

    @functools.wraps(f)
    def inner(*args, **kw):
        # time.sleep(0.1)
        return f(u, *args, **kw)

    return inner

@app.route("/")
@login_required
def index(u):
    return open("static/main.html").read()

@app.route("/shelves")
@login_required
def shelves(u):
    shelves = u.getAllShelves()
    return json.dumps([s.serialize() for s in shelves])

@app.route("/login")
def login():
    return "404"

if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost")
