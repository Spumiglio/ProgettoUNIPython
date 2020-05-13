from flask import Flask
from flask import request,g,session,jsonify
import sqlite3
import Operations

app = Flask(__name__)


db = None
def get_db():
    global db
    db = sqlite3.connect('database.db',check_same_thread=False)


@app.route('/login', methods=['GET','POST'])
def login():
    name = request.args.get("username")
    password = request.args.get("password")
    r = Operations.login(name,password,db)
    return r

@app.route('/register/<id>', methods=['GET','POST'])
def register(id):
    content = request.get_json(silent = True)
    print (content)
    r = Operations.register(id,content,db)
    return r

@app.route('/addProduct/<idu>', methods=['GET','POST'])
def addProduct(idu):
    content = request.get_json(silent=True)
    print (content)
    r = Operations.addProduct(idu,content,db)
    return r

@app.route('/getFirstProducts', methods=['GET','POST'])
def getFirstProducts():
    r = Operations.getFirstProducts(db)
    return jsonify(r)

@app.teardown_appcontext
def close_connection(Exception):
    dbc = getattr(g, '_database', None)
    if dbc is not None:
        dbc.close()

@app.errorhandler(Exception)
def unhandled_exception(e):

    app.logger.error('Unhandled Exception: %s', (e))
    return "ERROR 404"


if __name__ == "__main__":
    get_db()
    app.run()

