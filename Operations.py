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
            c.execute("INSERT INTO utenti VALUES (?,?,?,?,?,?,?,?,?,?,?)",(id, d["nome"], d["cognome"], d["telefono"], "<null>", "<null>", d["email"], d["password"], matricola, "<null>",d["ruolo"]))
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
            c.execute("INSERT INTO utenti VALUES (?,?,?,?,?,?,?,?,?,?,?)",(id,d["nome"],d["cognome"],d["telefono"],pag,ddp,d["email"],d["password"],matricola,tid,"<null>"))
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
    if u != [] and u[0][8] != "None":
        c.execute("INSERT INTO prodotti VALUES (?,?,?,?,?,?,?,?,?)",(d["id"],d["nome"],d["disponibilita"],d["prezzo"],d["immagine"],d["tag"],d["categoria"],d["marca"],d["quantita"]))
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
        c.execute("INSERT INTO tessere VALUES (?,?,?)",(d["id"],d["dataEmissione"],d["saldoPunti"]))
        c.execute("UPDATE utenti SET idtessera=? WHERE id=?",(d["id"],idu))
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
                c.execute("INSERT INTO ordini VALUES(?,?,?,?,?,?)",(idu,i["id"],data,i["quantita"],idOrdine,d["dataConsegna"]))
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
    nomep+="%"
    d = c.execute("SELECT * FROM prodotti p WHERE nome LIKE ?",(nomep,)).fetchall()
    if d != []:

        return jsonify(d)
    else:
        return "PRODOTTO INESISTENTE"


def getProdByTag(tag,db):
    r = []
    c = db.cursor()
    taglist = tag.split(";")

    for i in taglist:
        d = c.execute("SELECT * FROM prodotti p WHERE p.tag=?",(i,)).fetchall()
        r += d
    return jsonify(r)


def getProdByCat(cat,db):
    r = []
    c = db.cursor()
    catlist = cat.split(";")
    for i in catlist:
        d = c.execute("SELECT * FROM prodotti p WHERE p.categoria=?",(i,)).fetchall()
        r += d
    return jsonify(r)


def removeProdByID(pid,uid,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,))
    u = ver.fetchall()
    if u != [] and u[0][8] != "None":
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
    s = c.execute("SELECT idOrdine,dataConsegna FROM ordini WHERE id = ? AND data=? GROUP BY data", (uid,date))
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


def getProdByBrand(brand, db):
    c = db.cursor()
    brand+="%"
    d = c.execute("SELECT * FROM prodotti p WHERE marca LIKE ?", (brand,)).fetchall()
    if d != []:
        print(d)
        return jsonify(d)
    else:
        return "MARCA INESISTENTE"



def addQuantity(pid,uid,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,))
    u = ver.fetchall()
    if u != [] and u[0][8] != "None":
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
    if u != [] and u[0][8] != "None":
        verp = c.execute("SELECT * FROM prodotti p WHERE p.idprodotto=?", (pid,)).fetchall()
        if verp != []:
            qa = int(verp[0][2]) -1
            c.execute("UPDATE prodotti SET disponibilita=? WHERE idprodotto=?", (qa, pid))
            db.commit()
            s = "OK"
    else:
        s = "UTENTE NON AUTORIZZATO"
    return s


def addTesseraPoint(idt,punti,db):
    c = db.cursor()
    verp = c.execute("SELECT * FROM tessere t WHERE t.idtessera=?", (idt,)).fetchall()
    if verp != []:
        qa = int(verp[0][2]) + int(punti)
        c.execute("UPDATE tessere SET punti=? WHERE idtessera=?", (qa, idt))
        db.commit()
        s = "OK"
    else:
        s = "UTENTE NON AUTORIZZATO"
    return s

def changePassword(uid,oldPassw,newPassw,db):
    c = db.cursor()
    verp = c.execute("SELECT * FROM utenti WHERE id=?",(uid,)).fetchall()
    if verp != [] and verp[0][7] == oldPassw:
        c.execute("UPDATE utenti SET password=? WHERE id=?",(newPassw,uid))
        db.commit()
        s="OK"
    else:
        s="PASSWORD NON CORRETTA"
    return s

def getAllUserOrderID(uid,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,))
    u = ver.fetchall()
    if u != [] and u[0][8] != "None":
        r = c.execute("SELECT id FROM ordini GROUP BY id").fetchall()
        return jsonify(r)
    else:
        return "UTENTE NON AUTORIZZATO"

def updateUserInfo(uid,dict,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.id=?", (uid,)).fetchall()
    indirizzo = dict["indirizzo"]
    if ver != []:
        c.execute("UPDATE indirizzi SET via=?, CAP=?,localita=?,provincia=?,civico=? "
                  "WHERE id=?",(indirizzo["via"],indirizzo["cap"],indirizzo["localita"],indirizzo["provincia"],indirizzo["civico"],uid))
        c.execute("UPDATE utenti SET nome=?,cognome=?,telefono=? WHERE id=?",(dict["nome"],dict["cognome"],dict["telefono"],uid))
        db.commit()
        return "OK"
    return "UTENTE NON AUTORIZZATO"

def getAllDeliveryDate(db):
    c = db.cursor()
    r = c.execute("SELECT dataConsegna FROM ordini GROUP BY dataConsegna").fetchall()
    return jsonify(r)

def getProdById(id, db):
    c = db.cursor()
    id+="%"
    d = c.execute("SELECT * FROM prodotti p WHERE idprodotto LIKE ?", (id,)).fetchall()
    if d != []:
        print(d)
        return jsonify(d)
    else:
        return "ID INESISTENTE"

