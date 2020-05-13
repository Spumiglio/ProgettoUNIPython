
def register(id,d,db):
    c = db.cursor()
    ver = c.execute("SELECT * FROM utenti u WHERE u.username=?", (d["username"],))
    res = ver.fetchall()
    if res != []:
        s = "USERNAME GIA UTILIZZATO"
    else:
        c.execute("INSERT INTO utenti VALUES (?,?,?,?,?)",(id,d["username"],d["password"],d["numtel"],d["ruolo"]))
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
    if u[0][4] == "operatore":
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
