from flask import Flask
from flask import request, g, session, jsonify
import sqlite3
import Operations

app = Flask(__name__)

db = None


def get_db():
    global db
    db = sqlite3.connect('database.db', check_same_thread=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.args.get("email")
    password = request.args.get("password")
    r = Operations.login(email, password, db)
    return r


@app.route('/register/<id>', methods=['GET', 'POST'])
def register(id):
    content = request.get_json(silent=True)
    r = Operations.register(id, content, db)
    return r


@app.route('/addProduct/<uid>', methods=['GET', 'POST'])
def addProduct(uid):
    content = request.get_json(silent=True)
    r = Operations.addProduct(uid, content, db)
    return r


@app.route('/getFirstProducts', methods=['GET', 'POST'])
def getFirstProducts():
    r = Operations.getFirstProducts(db)
    return jsonify(r)


@app.route('/addTessera/<uid>', methods=['GET', 'POST'])
def addTessera(uid):
    content = request.get_json(silent=True)
    r = Operations.addTesseraFed(uid, db, content)
    return r


@app.route('/buyOrder/<uid>', methods=['GET', 'POST'])
def buyOrder(uid):
    content = request.get_json(silent=True)
    r = Operations.buyOrder(uid, db, content)
    return r


@app.route('/getAllOrders/<uid>', methods=['GET', 'POST'])
def getAllOrders(uid):
    r = Operations.getOrderById(uid, db)
    return jsonify(r)


@app.route('/getProdByName/<nomep>', methods=['GET', 'POST'])
def getProdByName(nomep):
    uid = request.args.get("uid")
    r = Operations.getProdByName(nomep, uid, db)
    return r


@app.route('/getProdByTag/<tag>', methods=['GET', 'POST'])
def getProdByTag(tag):
    uid = request.args.get("uid")
    r = Operations.getProdByTag(tag, uid, db)
    return r


@app.route('/getProdByCat/<cat>', methods=['GET', 'POST'])
def getProdByCat(cat):
    uid = request.args.get("uid")
    r = Operations.getProdByCat(cat, uid, db)
    return r


@app.route('/removeProdByName/<nomep>', methods=['GET', 'POST'])
def removeProdByName(nomep):
    uid = request.args.get("uid")
    r = Operations.removeProdByName(nomep, uid, db)
    return r


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
