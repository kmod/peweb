import time

try:
    import simplejson as json
except ImportError:
    import json

import flask
app = flask.Flask(__name__)

request = flask.request

_main_html = open("templates/main.html").read()

@app.route("/")
def index():
    return flask.redirect(flask.url_for('static', filename="main.html"))

@app.route("/shelves")
def shelves():
    shelves = {
            5: {
                "name": "test bookshelf",
                "papers": []
                }
            }
    return json.dumps(shelves)

cur_comments = [{'author': "Peter Hunt", 'text': "This is one comment"}, {'author': "Jordan Walke", 'text': "This is *another* comment"}]

@app.route("/comments.json", methods=["GET", "POST"])
def comments():
    if request.method == "POST":
        time.sleep(0.4)
        cur_comments.append(dict(request.form))

    return json.dumps(cur_comments)

if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost")
