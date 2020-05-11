from flask import Flask
from flask import request,g,session
import sqlite3
import Operations

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/login', methods=['GET','POST'])
def login():
    name = request.args.get("username")
    password = request.args.get("password")
    r = Operations.login(name,password,get_db())
    return r

@app.route('/register', methods=['GET','POST'])
def register():
    name = request.args.get("username")
    password = request.args.get("password")
    r = Operations.register(name,password,get_db())
    return r

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()

