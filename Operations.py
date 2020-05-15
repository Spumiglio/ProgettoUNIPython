from flask import jsonify
def register(id,d,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.username=?", (d["username"],))
    res = ver.fetchall()
    if res != []:
        s = "USERNAME GIA UTILIZZATO"
    else:
        c.execute("INSERT INTO utenti VALUES (?,?,?,?,?,?,?)",(id,d["username"],d["password"],d["numtel"],d["ruolo"],d["metodop"],d["datip"]))
        indirizzo = d["indirizzo"]
        c.execute("INSERT INTO indirizzi VALUES (?,?,?,?)",(id,indirizzo["via"],indirizzo["CAP"],indirizzo["citta"]))
        s = "OK"
    db.commit()
    return s

def login(username,password,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.username=? AND u.password=?", (username,password))
    res = ver.fetchall()
    if res == []:
        s = "LOGIN ERRATO"
    else:
        s = res[0][0]
    return s

def addProduct(idu,d,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (idu,))
    u = ver.fetchall()
    if u != [] and u[0][7] != "None":
        c.execute("INSERT INTO prodotti VALUES (?,?,?,?)",(d["idp"],d["nomep"],d["quantitap"],d["prezzop"],d["immaginep"]))
        db.commit()
        s= "OK"
    else:
        s = "UTENTE NON AUTORIZZATO"
    return s

def getFirstProducts(db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM prodotti ORDER BY CAST(quantita AS INTEGER) DESC LIMIT 10")
    d = ver.fetchall()
    return d

def addTesseraFed(idu,db,d):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (idu,))
    u = ver.fetchall()
    if u != []:
        c.execute("INSERT INTO tessere VALUES (?,?,?)",(idu,d["data"],d["punti"]))
        db.commit()
        s = "OK"
    else:
        s = "UTENTE NON TROVATO"
    return s

def buyOrder(idu,db,d):
    s = ""
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (idu,))
    u = ver.fetchall()
    if u != []:
        for i in d.values():
            verp = c.execute("SELECT * FROM prodotti p WHERE p.idprodotto=?",(i["idp"],)).fetchall()
            print (i["quantita"],verp[0][2])
            if verp != [] and  int(verp[0][2]) >= int(i["quantita"]):
                c.execute("INSERT INTO ordini VALUES(?,?,?,?)",(idu,i["idp"],i["data"],i["quantita"]))
                qa = int(verp[0][2]) - int(i["quantita"])
                c.execute("UPDATE prodotti SET quantita=? WHERE idprodotto=?",(qa,i["idp"]))
                db.commit()
                s = "OK"
            else:
                s += "PRODOTTO NON DISPONIBILE: " + verp[0][1] +"\n "

    else:
        s = "UTENTE NON TROVATO"
    return s


def getOrderById(idu,db):
    c = db.cursor()
    d = c.execute("SELECT idprodotto,data,quantita FROM ordini WHERE id = ? ORDER BY idprodotto",(idu,))
    return d.fetchall()

def getProdByName(nomep,uid,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?",(uid,)).fetchall()
    if ver != []:
        d = c.execute("SELECT * FROM prodotti p WHERE p.nome=?",(nomep,)).fetchall()
        if d != []:
            print(d)
            return jsonify(d)
        else:
            return "PRODOTTO INESISTENTE"
    else:
        return "UTENTE NON AUTORIZZATO"

def getProdByTag(tag,uid,db):
    r = []
    c = db.cursor()
    taglist = tag.split(";")
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,)).fetchall()
    if ver != []:
        for i in taglist:
            d = c.execute("SELECT * FROM prodotti p WHERE p.tag=?",(i,)).fetchall()
            r += d
        return jsonify(r)
    else:
        return "UTENTE NON AUTORIZZATO"

def getProdByCat(cat,uid,db):
    r = []
    c = db.cursor()
    catlist = cat.split(";")
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,)).fetchall()
    if ver != []:
        for i in catlist:
            d = c.execute("SELECT * FROM prodotti p WHERE p.categoria=?",(i,)).fetchall()
            r += d
        return jsonify(r)
    else:
        return "UTENTE NON AUTORIZZATO"

def removeProdByName(name,uid,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,))
    u = ver.fetchall()
    if u != [] and u[0][7] != "None":
        c.execute("DELETE FROM prodotti WHERE nome=?",(name,))
        db.commit()
        s = "OK"
    else:
        s = "UTENTE NON AUTORIZZATO"
    return s