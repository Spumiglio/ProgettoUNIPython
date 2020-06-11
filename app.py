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
    print (r)
    return r


@app.route('/register/<id>', methods=['GET', 'POST'])
def register(id):
    content = request.get_json(silent=True)
    print (content)
    r = Operations.register(id, content, db)
    return r


@app.route('/addProduct/<uid>', methods=['GET', 'POST'])
def addProduct(uid):
    content = request.get_json(silent=True)
    print(content)
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
    print(content)
    r = Operations.buyOrder(uid, db, content)
    return r

@app.route('/getProdByBrand/<brand>')
def getProdByBrand(brand):
    r = Operations.getProdByBrand(brand,db)
    return r


@app.route('/getAllProdByOrder/<uid>', methods=['GET', 'POST'])
def getAllOrders(uid):
    data = request.args.get("date")
    r = Operations.getOrderById(uid,data,db)
    return jsonify(r)

@app.route('/getAllOrdersDate/<uid>', methods=['GET', 'POST'])
def getAllOrdersDate(uid):
    r = Operations.getAllOrderDate(uid,db)
    print(r)
    return jsonify(r)

@app.route('/getOrderID/<uid>', methods=['GET', 'POST'])
def getOrderID(uid):
    data = request.args.get("date")
    r = Operations.getOrderID(uid,db,data)
    return jsonify(r)


@app.route('/getProdByName/<nomep>', methods=['GET', 'POST'])
def getProdByName(nomep):
    r = Operations.getProdByName(nomep,db)
    return r


@app.route('/getProdByTag/<tag>', methods=['GET', 'POST'])
def getProdByTag(tag):
    r = Operations.getProdByTag(tag,db)
    return r


@app.route('/getProdByCat/<cat>', methods=['GET', 'POST'])
def getProdByCat(cat):
    r = Operations.getProdByCat(cat,db)
    return r


@app.route('/removeProd/<idp>', methods=['GET', 'POST'])
def removeProdByID(idp):
    uid = request.args.get("uid")
    r = Operations.removeProdByID(idp, uid, db)
    return r

@app.route('/getUserInfo/<idu>',methods=['GET','POST'])
def getUserInfo(idu):
    r = Operations.getUserInfo(idu,db)
    return jsonify(r)

@app.route('/addQuantity/<idp>', methods=['GET','POST'])
def addQuantity(idp):
    uid = request.args.get("uid")
    r = Operations.addQuantity(idp,uid,db)
    return r

@app.route('/removeQuantity/<idp>', methods=['GET','POST'])
def removeQuantity(idp):
    uid = request.args.get("uid")
    r = Operations.removeQuantity(idp,uid,db)
    return r

@app.route('/addPoint/<idt>', methods=['GET','POST'])
def addTesseraPoint(idt):
    punti = request.args.get("punti")
    r= Operations.addTesseraPoint(idt,punti,db)
    return r

@app.route('/changePassword/<uid>', methods=['GET','POST'])
def changePassword(uid):
    oldPassw = request.args.get("old")
    newPassw = request.args.get("new")
    r = Operations.changePassword(uid,oldPassw,newPassw,db)
    return r

@app.route('/getAllUserID/<uid>', methods=['GET','POST'])
def getAllUserID(uid):
    r = Operations.getAllUserOrderID(uid,db)
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
    app.run(host='0.0.0.0', port='9440')
