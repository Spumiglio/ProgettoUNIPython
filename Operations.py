from flask import jsonify
def register(id,d,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.email=?", (d["email"],))
    res = ver.fetchall()
    indirizzo = d["indirizzo"]
    if res != []:
        s = "USERNAME GIA UTILIZZATO"
    else:
        if "matricola" in d:
            matricola = d["matricola"]
            c.execute("INSERT INTO utenti VALUES (?,?,?,?,?,?,?,?,?,?)",(id, d["nome"], d["cognome"], d["telefono"], "<null>", "<null>", d["email"], d["password"], matricola, "<null>"))
        else:
            matricola = "<null>"
            if "tesseraFedelta" in d:
                tesserafed = d["tesseraFedelta"]
                c.execute("INSERT INTO tessere VALUES (?,?,?)",(tesserafed["id"], tesserafed["dataEmissione"], tesserafed["saldoPunti"]))
                tid = tesserafed["id"]
            else:
                tid = "<null>"
            if d["pagamento"] == "CONSEGNA":
                ddp = "<null>"
            else:
                ddp = d["datiDelPagamento"]

            if "pagamento" in d:
                pag = d["pagamento"]
            else:
                pag = "<null>"
            c.execute("INSERT INTO utenti VALUES (?,?,?,?,?,?,?,?,?,?)",(id,d["nome"],d["cognome"],d["telefono"],pag,ddp,d["email"],d["password"],matricola,tid))
        c.execute("INSERT INTO indirizzi VALUES (?,?,?,?,?,?,?)",(id,indirizzo["via"],indirizzo["cap"],indirizzo["localita"],indirizzo["provincia"],indirizzo["paese"],indirizzo["civico"]))

        s = "OK"
    db.commit()
    return s

def login(email,password,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.email=? AND u.password=?", (email,password))
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
    ver = c.execute("SELECT * FROM prodotti ORDER BY CAST(disponibilita AS INTEGER) DESC LIMIT 10")
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
    data = d["data"]
    idOrdine = d["ID"]
    listaprodotti = d["prodotti"]

    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (idu,))
    u = ver.fetchall()
    if u != []:
        for i in listaprodotti:
            verp = c.execute("SELECT * FROM prodotti p WHERE p.idprodotto=?",(i["id"],)).fetchall()
            if verp != [] and  int(verp[0][2]) >= int(i["quantita"]):
                c.execute("INSERT INTO ordini VALUES(?,?,?,?,?)",(idu,i["id"],data,i["quantita"],idOrdine))
                qa = int(verp[0][2]) - int(i["quantita"])
                c.execute("UPDATE prodotti SET disponibilita=? WHERE idprodotto=?",(qa,i["id"]))
                db.commit()
                s = "OK"
            else:
                s += "PRODOTTO NON DISPONIBILE: " + verp[0][1] +"\n "

    else:
        s = "UTENTE NON TROVATO"
    return s


def getOrderById(idu,date,db):
    c = db.cursor()
    d = c.execute("SELECT idprodotto,data,quantita FROM ordini WHERE id = ? AND data = ? ORDER BY idprodotto",(idu,date))
    r = []
    for i in d.fetchall():
        e = c.execute("SELECT * FROM prodotti WHERE idprodotto =? ",(i[0],))
        a = e.fetchall()
        b=list(a.pop(0))
        b.insert(8,i[2])
        a.append(tuple(b))
        r+= a
    return r

def getProdByName(nomep,db):
    c = db.cursor()
    d = c.execute("SELECT * FROM prodotti p WHERE p.nome=?",(nomep,)).fetchall()
    if d != []:
        print(d)
        return jsonify(d)
    else:
        return "PRODOTTO INESISTENTE"


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

def removeProdByID(pid,uid,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,))
    u = ver.fetchall()
    if u != [] and u[0][7] != "None":
        c.execute("DELETE FROM prodotti WHERE idprodotto=?",(pid,))
        db.commit()
        s = "OK"
    else:
        s = "UTENTE NON AUTORIZZATO"
    return s

def getAllOrderDate(uid,db):
    c = db.cursor()
    s = c.execute("SELECT data,idOrdine FROM ordini WHERE id = ? GROUP BY data",(uid,))
    r = s.fetchall();
    return r

def getOrderID(uid,db,date):
    c = db.cursor()
    s = c.execute("SELECT idOrdine FROM ordini WHERE id = ? AND data=? GROUP BY data", (uid,date))
    r = s.fetchall();
    return r

def getUserInfo(uid,db):
    c = db.cursor()
    u = c.execute("SELECT * FROM utenti WHERE id = ? ", (uid,)).fetchall()
    i = c.execute("SELECT * FROM indirizzi WHERE id=?",(uid,)).fetchall()
    if u[0][9] != "<null>":
        t = c.execute("SELECT * FROM tessere WHERE idtessera=?",(u[0][9],)).fetchall()
        r=u+i+t
    else:
        r = u+i
    return r


def getProdByBrand(brand, uid, db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,)).fetchall()
    if ver != []:
        d = c.execute("SELECT * FROM prodotti p WHERE p.marca=?", (brand,)).fetchall()
        if d != []:
            return jsonify(d)
        else:
            return "MARCA INESISTENTE"
    else:
        return "UTENTE NON AUTORIZZATO"


def addQuantity(pid,uid,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,))
    u = ver.fetchall()
    if u != [] and u[0][7] != "None":
        verp = c.execute("SELECT * FROM prodotti p WHERE p.idprodotto=?", (pid,)).fetchall()
        if verp != []:
            qa = int(verp[0][2]) + 1
            c.execute("UPDATE prodotti SET disponibilita=? WHERE idprodotto=?", (qa, pid))
            db.commit()
            s = "OK"
    else:
        s = "UTENTE NON AUTORIZZATO"
    return s

def removeQuantity(pid,uid,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,))
    u = ver.fetchall()
    if u != [] and u[0][7] != "None":
        verp = c.execute("SELECT * FROM prodotti p WHERE p.idprodotto=?", (pid,)).fetchall()
        if verp != []:
            qa = int(verp[0][2]) -1
            c.execute("UPDATE prodotti SET disponibilita=? WHERE idprodotto=?", (qa, pid))
            db.commit()
            s = "OK"
    else:
        s = "UTENTE NON AUTORIZZATO"
    return s
