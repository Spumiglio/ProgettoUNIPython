
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