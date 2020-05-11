from flask import Flask
from flask import request,g,session
import sqlite3

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/login', methods=['GET'])
def login():
    name = request.args.get("username")
    password = request.args.get("password")


if __name__ == '__main__':
    app.run()

