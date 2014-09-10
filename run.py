try:
    import simplejson as json
except ImportError:
    import json

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/shelves")
def shelves():
    shelves = {
            5: {
                "name": "test bookshelf",
                "papers": []
                }
            }
    return json.dumps(shelves)

@app.route("/comments.json")
def comments():
    return """[
    {author: "Pete Hunt", text: "This is one comment"},
    {author: "Jordan Walke", text: "This is *another* comment"}
    ]"""

if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost")
